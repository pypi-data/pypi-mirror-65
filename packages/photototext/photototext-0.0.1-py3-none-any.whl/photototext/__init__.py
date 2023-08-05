import numpy as np
from PIL import Image


def change(image_file):
    # ��ͼƬ�ļ�
    image = Image.open(image_file)
    # ��ȡͼƬrect����
    image_width, image_height = image.size
    # ͼƬ�¿��
    width = 200
    # ͼƬ�¸߶�
    height = int(image_height / (image_width / width) / 2)
    # ѹ��ͼƬ
    image = image.resize((width, height), Image.ANTIALIAS)
    # ��ͼƬ�޸�Ϊ�ڰ�ģʽ
    image = image.convert('L')
    # �����ַ���
    str = 'MNHQ$OC?7>!:-;. '
    # �����ַ���
    text = ""
    # ��ȡͼƬ����ֵ
    pixel = np.array(image)
    # ͼƬת�ַ�
    for h in range(height):
        # �����б�
        for w in range(width):
            # ����ַ�
            text += str[pixel[h][w] // 16]
        # ����
        text += '\n'
    # ������ֵ
    return text