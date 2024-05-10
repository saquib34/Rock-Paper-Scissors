"""
Module for Rock-Paper-Scissors game.
"""
import time
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector


def run_game():
    """
    Main function to run the Rock-Paper-Scissors game.
    """
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    detector = HandDetector(maxHands=1)
    timer_val = 0
    state_result = False
    start_game = False
    score = [0, 0]  # [computer, player]

    init_time = time.time()
    while True:
        img_bg = cv2.imread('Resources/BG.png')
        success, img = cap.read()
        img_scaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
        img_scaled = img_scaled[:, 80:480]
        hands, img = detector.findHands(img_scaled)

        if start_game:
            if not state_result:
                timer_val = time.time() - init_time
                cv2.putText(img_bg, str(int(timer_val)), (605, 435),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
                if timer_val > 3:
                    state_result = True
                    timer_val = 0
                    play_move = None
                    if hands:
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        if fingers == [0, 0, 0, 0, 0]:
                            play_move = 1
                            print("ROCK")
                        elif fingers == [1, 1, 1, 1, 1]:
                            play_move = 2
                            print("PAPER")
                        elif fingers == [0, 1, 1, 0, 0]:
                            play_move = 3
                            print("SCISSOR")
                        print(fingers)

                    computer_move = random.randint(1, 3)
                    img_ai = cv2.imread(f'Resources/{computer_move}.png', cv2.IMREAD_UNCHANGED)
                    img_bg = cvzone.overlayPNG(img_bg, img_ai, (149, 310))

                    if (play_move == 1 and computer_move == 2) or \
                       (play_move == 3 and computer_move == 1) or \
                       (play_move == 2 and computer_move == 3):
                        score[0] += 1
                        print("Computer Win")
                    elif (play_move == 1 and computer_move == 3) or \
                         (play_move == 2 and computer_move == 1) or \
                         (play_move == 3 and computer_move == 2):
                        score[1] += 1

            img_bg[233:653, 795:1195] = img_scaled

            if state_result:
                img_bg = cvzone.overlayPNG(img_bg, img_ai, (149, 310))
                cv2.putText(img_bg, str(score[0]), (410, 215),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5)
                cv2.putText(img_bg, str(score[1]), (1112, 215),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5)

        cv2.imshow("BG", img_bg)
        key_ = cv2.waitKey(1)

        if key_ == ord('s'):
            start_game = True
            init_time = time.time()
            state_result = False
        elif key_ == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()

