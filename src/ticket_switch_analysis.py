import csv, json, os
import cv2

img_folder_path = '/home/zhangxing/Downloads/2018-12-5_8.3K/images/'
result_file_path = "output/ts_result_legacy_2018-12-12_13:42:34.csv"
# result_file_path = "output/ts_result_legacy.csv"
ts_output_path = 'ticket_switch_imgs/'
none_ts_output_path = 'none_ticket_switch_imgs/'
multi_product_imgs = 'multi_product_imgs/'
save_mode = '.jpg'

rgb_a = (0, 255, 0)
rgb_b = (255, 0, 0)


def get_real_pos(img_np, positions):
    _full_image_height, _full_image_width = img_np.shape[:2]
    real_pos = []
    for item in positions:
        item[0] = int(item[0] * _full_image_width)
        item[1] = int(item[1] * _full_image_height)
        real_pos.append(item)
    return real_pos


def draw(img_np, positions, rgb):
    for i in range(len(positions)):
        p1 = positions[i]
        p2 = positions[0] if (i + 1) == len(positions) else positions[i + 1]
        cv2.line(img_np, (p1[0], p1[1]), (p2[0], p2[1]), rgb, 5)


def draw_lines(filename, detect_result, ticket_switch):
    try:
        img = cv2.imread(img_folder_path + filename, cv2.IMREAD_COLOR)
        output_path = ts_output_path if ticket_switch == 1 else none_ts_output_path
        # 单框
        if 'product_positions' in detect_result[0]:
            product_positions = get_real_pos(img, detect_result[0]['product_positions'])
            draw(img, product_positions, rgb_a)
        # 扫码床
        if 'scanning_bed_key_points' in detect_result[0]:
            scanning_bed_key_points = get_real_pos(img, detect_result[0]['scanning_bed_key_points'])
            draw(img, scanning_bed_key_points, rgb_b)
        # 多框
        if 'multi_product_positions' in detect_result[0]:
            multi_product_positions = detect_result[0]['multi_product_positions']
            for pos in multi_product_positions:
                real_pos = get_real_pos(img, pos)
                draw(img, real_pos, rgb_a)
            output_path += multi_product_imgs

        if save_mode:
            filename = os.path.splitext(filename)[0] + save_mode
        cv2.imwrite(output_path + filename, img)

    finally:
        pass


def analysis(result_file_path):
    with open(result_file_path) as f:
        csv_reader = csv.reader(f)
        for item in csv_reader:
            success = int(item[0])
            ticket_switch = -1 if item[3] == '' else int(item[3])
            if success == 1 and ticket_switch == 0:
                info = json.loads(item[-1])
                filename = item[1]
                detect_result = info['results']
                draw_lines(filename, detect_result, ticket_switch)


if __name__ == '__main__':
    # 找到csv中指定图片，打框输出
    analysis(result_file_path)
