#!/usr/bin/env python3
"""Offline PC horizontal hipfire conversion; confidence travels with the result."""
import argparse
import json
import math
from pathlib import Path


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError('must be finite and greater than zero')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from', dest='source')
    parser.add_argument('--to', dest='target')
    parser.add_argument('--dpi', type=positive)
    parser.add_argument('--sens', type=positive)
    parser.add_argument('--to-dpi', type=positive)
    parser.add_argument('--calibrate-current', type=positive)
    parser.add_argument('--measured-cm', type=positive)
    parser.add_argument('--desired-cm', type=positive)
    args = parser.parse_args()
    calibration = [args.calibrate_current, args.measured_cm, args.desired_cm]
    if any(x is not None for x in calibration):
        if not all(x is not None for x in calibration):
            parser.error('calibration requires current sensitivity, measured cm and desired cm')
        print(json.dumps({'sensitivity': args.calibrate_current * args.measured_cm / args.desired_cm,
                          'condition': 'locally linear scale, unchanged DPI/FOV/MDC/multipliers; remeasure after adjustment'}))
        return
    if any(x is None for x in [args.source, args.target, args.dpi, args.sens]):
        parser.error('conversion requires --from --to --dpi --sens')
    data = json.loads((Path(__file__).resolve().parents[1] / 'references/games.json').read_text())
    def resolve(value):
        for game in data['games']:
            if value.casefold() in [x.casefold() for x in [game['id'], game['name'], *game['aliases']]]:
                return game
        parser.error('unsupported game: ' + value)
    source, target = resolve(args.source), resolve(args.target)
    target_dpi = args.to_dpi or args.dpi
    result = args.sens * source['yaw'] / target['yaw'] * args.dpi / target_dpi
    warnings = []
    for game in [source, target]:
        if game['status'] != 'cross_checked':
            warnings.append(game['name'] + ': ' + game['status'] + '; consult references/sources.md')
    out = {'source': source['name'], 'target': target['name'], 'target_dpi': target_dpi,
           'target_sensitivity': result, 'rounded_3dp': round(result, 3),
           'cm_per_360': 914.4 / (args.dpi * args.sens * source['yaw']),
           'scope': data['scope'], 'checked_on': data['checked_on'],
           'source_status': source['status'], 'target_status': target['status'],
           'target_unit': target['unit'], 'warnings': warnings}
    if 'delta-force' in [source['id'], target['id']]:
        out['warning'] = 'Provisional KovaaK model, NOT verified exact Delta Force settings; MDC/FOV/horizontal multiplier may alter result.'
        if target['id'] == 'delta-force':
            out['alternative_aiming_pro_model'] = args.sens * source['yaw'] / .01 * args.dpi / target_dpi
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
