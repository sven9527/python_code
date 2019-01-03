import csv, json, os
import cv2

img_folder_path = 'output/'


rgb_a = (0, 255, 0)
rgb_b = (255, 0, 0)


def get_real_pos(img_np, positions):
    _full_image_height, _full_image_width = img_np.shape[:2]
    real_pos = []
    for item in positions:
        item[0] = int(item[0] * _full_image_width)
        item[1] = int(item[1] * _full_image_height)
        real_pos.append(item)

    #     left top width height

    return real_pos


def draw(img_np, positions, rgb):
    for i in range(len(positions)):
        p1 = positions[i]
        p2 = positions[0] if (i + 1) == len(positions) else positions[i + 1]
        cv2.line(img_np, (p1[0], p1[1]), (p2[0], p2[1]), rgb, 5)


def draw_lines(filename, detect_result):
    try:
        img = cv2.imread(img_folder_path + filename, cv2.IMREAD_COLOR)

        product_positions = get_real_pos(img, detect_result['box'])
        draw(img, product_positions, rgb_a)

        cv2.imwrite(img_folder_path + "corn_test.png", img)

    finally:
        pass


def analysis():

    detect_result = {
        # "box": [
        #     [0.11248505115509033, 0.0719480812549591],
        #     [0.8584395051002502, 0.0719480812549591],
        #     [0.8584395051002502, 0.8418596982955933],
        #     [0.11248505115509033, 0.8418596982955933]
        # ]
        "box": [
            [0.5743005275726318, 0.29702526330947876],
            [0.9283171892166138, 0.29702526330947876],
            [0.9283171892166138, 0.5898801684379578],
            [0.5743005275726318, 0.5898801684379578]
        ]
    }
    draw_lines("car.jpeg", detect_result)


if __name__ == '__main__':
    analysis()
