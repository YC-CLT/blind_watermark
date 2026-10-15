import argparse
from .blind_watermark import WaterMark


def cmd_embed(args):
    bwm = WaterMark(
        password_img=args.password_img,
        password_wm=args.password_wm,
        block_shape=tuple(args.block_shape),
        mode=args.core_mode,
        processes=args.processes,
    )
    bwm.read_img(filename=args.image)

    wm_mode = _resolve_wm_mode(args)
    bwm.read_wm(wm_content=args.watermark, mode=wm_mode)

    bwm.embed(filename=args.output, compression_ratio=args.compress)

    if wm_mode == 'str':
        print(f'Embed succeed! -> {args.output}')
        print(f'Watermark length (bits): {len(bwm.wm_bit)}')
    else:
        print(f'Embed succeed! -> {args.output}')
        print(f'Watermark shape: {args.watermark}')


def cmd_extract(args):
    bwm = WaterMark(
        password_img=args.password_img,
        password_wm=args.password_wm,
        block_shape=tuple(args.block_shape),
        mode=args.core_mode,
        processes=args.processes,
    )

    wm_mode = _resolve_wm_mode(args)

    if wm_mode in ('str', 'bit'):
        result = bwm.extract(
            filename=args.image,
            wm_shape=_parse_shape(args.wm_shape),
            mode=wm_mode,
        )
    else:
        result = bwm.extract(
            filename=args.image,
            wm_shape=_parse_shape(args.wm_shape),
            mode='img',
            out_wm_name=args.output,
        )

    if wm_mode == 'str':
        print(f'Extract succeed! Watermark:')
        print(result)
    elif wm_mode == 'bit':
        print(f'Extract succeed! Watermark bits:')
        print(result.tolist())
    else:
        print(f'Extract succeed! -> {args.output}')


def _resolve_wm_mode(args):
    if args.watermark_mode:
        return args.watermark_mode
    if hasattr(args, 'watermark') and args.watermark:
        import os
        if os.path.isfile(args.watermark):
            return 'img'
    return 'str'


def _parse_shape(shape_str):
    parts = shape_str.split(',')
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    if len(parts) == 1:
        return int(parts[0])
    raise argparse.ArgumentTypeError(f'Invalid shape: {shape_str}, use like "64" or "64,64"')


def _add_common_args(parser):
    parser.add_argument('--pwd-img', dest='password_img', type=int, default=1,
                        help='Password for image (default: 1)')
    parser.add_argument('--pwd-wm', dest='password_wm', type=int, default=1,
                        help='Password for watermark (default: 1)')
    parser.add_argument('--block-shape', dest='block_shape', type=int, nargs=2, default=(4, 4), metavar=('H', 'W'),
                        help='Block shape for embedding (default: 4 4)')
    parser.add_argument('--core-mode', dest='core_mode', default='common',
                        help='Core mode (default: common)')
    parser.add_argument('--processes', type=int, default=None,
                        help='Number of parallel processes')


def main():
    parser = argparse.ArgumentParser(
        prog='blind_watermark',
        description='Blind Watermark - embed/extract invisible watermarks in images',
    )
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 0.4.4')

    sub = parser.add_subparsers(dest='command', title='commands')

    p_embed = sub.add_parser('embed', help='Embed watermark into image')
    p_embed.add_argument('image', help='Path to original image')
    p_embed.add_argument('watermark', help='Watermark text, or path to watermark image')
    p_embed.add_argument('output', nargs='?', default='embedded.png',
                         help='Output image path (default: embedded.png)')
    p_embed.add_argument('--wm-mode', dest='watermark_mode', choices=('str', 'img', 'bit'), default=None,
                         help='Watermark mode (default: auto-detect)')
    p_embed.add_argument('-c', '--compress', type=int, default=None,
                         help='Compression ratio (0-100, smaller = more compressed)')
    _add_common_args(p_embed)
    p_embed.set_defaults(func=cmd_embed)

    p_extract = sub.add_parser('extract', help='Extract watermark from image')
    p_extract.add_argument('image', help='Path to watermarked image')
    p_extract.add_argument('wm_shape', help='Watermark shape, e.g. "111" or "64,64"')
    p_extract.add_argument('-o', '--output', default=None,
                           help='Output watermark image path (for img mode)')
    p_extract.add_argument('--wm-mode', dest='watermark_mode', choices=('str', 'img', 'bit'), default=None,
                           help='Watermark mode (default: str if no output; img if output specified)')
    _add_common_args(p_extract)
    p_extract.set_defaults(func=cmd_extract)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == '__main__':
    main()