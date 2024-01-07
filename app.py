import streamlit as st
import face_recognition
from PIL import Image, ImageDraw

# サンプル画像のパスを設定します。
sample_images = {
    "男性": "image/human/man.jpg",
    "女性": "image/human/woman.jpg",
    "三銃士": "image/human/three_musketeers.jpg"
}

# 事前に絵文字の画像を準備します
emoji_images = {
    "😀": "image/emoji/grinning.png",
    "😁": "image/emoji/smiling.png",
    "😅": "image/emoji/sweat.png"
}

selected_sample_image = st.selectbox("サンプル画像", ("男性", "女性", "三銃士"))
emoji = st.selectbox("顔文字", ("😀", "😁", "😅"))

image_path = sample_images[selected_sample_image]
image = Image.open(image_path)
st.image(image, caption='入力画像', use_column_width=True)

if st.button("実行"):

    load_image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(load_image)

    processed_image = image.copy()
    draw = ImageDraw.Draw(processed_image)

    # 絵文字画像の読み込み
    emoji_image = Image.open(emoji_images[emoji])
    for (top, right, bottom, left) in face_locations:
        # 顔のサイズを計算
        face_width = right - left
        face_height = bottom - top

        # 絵文字画像のサイズを顔のサイズに調整
        emoji_image_resized = emoji_image.resize((face_width, face_height))
        
        # 絵文字画像のモードをRGBAに変更（透明度情報を持たせる）
        emoji_image_resized = emoji_image_resized.convert("RGBA")

        # 描画先画像（processed_image）の該当部分をRGBAモードの新しい画像として取得
        temp_image = Image.new("RGBA", (face_width, face_height))
        temp_image.paste(processed_image.crop((left, top, right, bottom)), (0, 0))

        # 絵文字画像を一時的な画像に合成
        temp_image = Image.alpha_composite(temp_image, emoji_image_resized)

        # 一時的な画像を最終的な画像にペースト
        processed_image.paste(temp_image, (left, top), temp_image)

    # 結果を表示
    st.image(processed_image, caption='結果画像', use_column_width=True)
