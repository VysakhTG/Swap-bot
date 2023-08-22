from pyrogram import Client, filters
from pyrogram.raw.types import InputFile
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import cv2
import dlib
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')



@Client.on_message(filters.command("faceswap"))
async def start(client, query):
    await client.send_message(
        query.from_user.id,
        "Do you want to continue with face swapping?",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Continue", callback_data="start")]]
        )
    )

@Client.on_callback_query(filters.regex("start"))
async def startswap(client, query):
    chat_id = query.message.chat.id
    chat_id = query.from_user.id

    first_photo = await client.ask(identifier = (chat_id, chat_id, None), text="send first photo")
    second_photo = await client.ask(identifier = (chat_id, chat_id, None), text="send second photo")
    await perform_face_swapping(client, chat_id, user_id, first_photo.photo.file_id, second_photo.photo.file_id)
            

async def perform_face_swapping(bot, chat_id, user_id, first_photo, second_photo):
    first_image = await bot.download_media(first_photo)
    second_image = await bot.download_media(second_photo)

    image1 = cv2.imread(first_image)
    image2 = cv2.imread(second_image)

    landmarks1 = get_landmarks(image1)
    landmarks2 = get_landmarks(image2)

    if landmarks1 is None or landmarks2 is None:
        await bot.send_message(chat_id, "Failed to detect landmarks in one or both images.")
        return
    swapped_image = warp_and_blend_faces(image1, landmarks1, image2, landmarks2)
    result_path = "result.jpg"
    cv2.imwrite(result_path, swapped_image)
    await bot.send_photo(chat_id, photo=InputFile(result_path), caption="Here's your face-swapped image.")

def get_landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    if len(faces) == 0:
        return None
    
    landmarks = predictor(gray, faces[0])
    return landmarks

def warp_and_blend_faces(image1, landmarks1, image2, landmarks2):
    landmarks1 = np.array([(p.x, p.y) for p in landmarks1.parts()])
    landmarks2 = np.array([(p.x, p.y) for p in landmarks2.parts()])
    
    mask = np.zeros_like(image2)
    mask = cv2.fillConvexPoly(mask, landmarks2, (255, 255, 255))
    
    transformation_matrix = cv2.estimateAffinePartial2D(landmarks2, landmarks1)[0]
    
    warped_image = cv2.warpAffine(image2, transformation_matrix, (image1.shape[1], image1.shape[0]))
    
    blended_image = cv2.seamlessClone(warped_image, image1, mask, (100, 100), cv2.NORMAL_CLONE)
    return blended_image
