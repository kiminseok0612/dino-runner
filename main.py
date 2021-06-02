import pygame
import os
import random

# 장애물 생성하는 함수
def add_box(box,box_img):
    max_x_pos=0
    for i, val in enumerate(box):
        if max_x_pos < val["x_pos"]:
            max_x_pos=val["x_pos"]
    max_x_pos+=random.randrange(200,401)
    box_idx=random.randrange(0,2)
    if box_idx==0:
        y_pos=128
    else:
        y_pos=75

    add_object={
        "img":box_img[box_idx],
        "x_pos":max_x_pos,
        "y_pos":y_pos
    }
    return add_object

pygame.init()
screen=pygame.display.set_mode((480,192))
pygame.display.set_caption("DINO RUNNER")
clock=pygame.time.Clock()
file_path=os.path.dirname(__file__)
image_path=os.path.join(file_path,("image"))
game_font=pygame.font.Font(None,25)

background=[
    {"img":pygame.image.load(os.path.join(image_path,"background.png")),"x_pos":0},
    {"img":pygame.image.load(os.path.join(image_path,"background.png")),"x_pos":480},
]
game_speed=10 # 장애물들의 속도
length=0

# 공룡 초기화
dino_img=[ # 공룡 이미지
    pygame.image.load(os.path.join(image_path,"dino1.png")), # 달리기
    pygame.image.load(os.path.join(image_path,"dino2.png")),
    pygame.image.load(os.path.join(image_path,"dino3.png")),
    pygame.image.load(os.path.join(image_path,"dino4.png")),
    pygame.image.load(os.path.join(image_path,"dino5.png")),
    pygame.image.load(os.path.join(image_path,"dino6.png")),
    pygame.image.load(os.path.join(image_path,"dino7.png")),
    pygame.image.load(os.path.join(image_path,"dino8.png")),
    pygame.image.load(os.path.join(image_path,"dino9.png")),
    pygame.image.load(os.path.join(image_path,"dino10.png")),
    pygame.image.load(os.path.join(image_path,"dino11.png")),
    pygame.image.load(os.path.join(image_path,"dino12.png")),
    pygame.image.load(os.path.join(image_path,"dino_down1.png")), # 엎드리기
    pygame.image.load(os.path.join(image_path,"dino_down2.png")),
    pygame.image.load(os.path.join(image_path,"dino_down3.png")),
    pygame.image.load(os.path.join(image_path,"dino_down4.png")),
    pygame.image.load(os.path.join(image_path,"dino_down5.png")),
    pygame.image.load(os.path.join(image_path,"dino_down6.png")),
    pygame.image.load(os.path.join(image_path,"dino_down7.png")),
    pygame.image.load(os.path.join(image_path,"dino_down8.png")),
    pygame.image.load(os.path.join(image_path,"dino_down9.png")),
    pygame.image.load(os.path.join(image_path,"dino_down10.png")),
    pygame.image.load(os.path.join(image_path,"dino_down11.png")),
    pygame.image.load(os.path.join(image_path,"dino_down12.png")),
    pygame.image.load(os.path.join(image_path,"dino_jump.png")), # 점프 
    pygame.image.load(os.path.join(image_path,"dino_die.png")), # 게임오버
    pygame.image.load(os.path.join(image_path,"dino_down_die.png")), # 엎드리기 후 게임오버
    pygame.image.load(os.path.join(image_path,"dino_jump_die.png")), # 점프 후 게임오버
]
dino_img_idx=0
dino_size=dino_img[dino_img_idx].get_rect().size
dino_x_pos=32
dino_y_pos=160-dino_size[1]
dino_down=False
dino_jump=False

# 장애물 이미지
box_img=[
    pygame.image.load(os.path.join(image_path,"box1.png")),
    pygame.image.load(os.path.join(image_path,"box2.png")),
]
box=[]

# 메인 루프
run=True
while run:
    fps=clock.tick(24)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_DOWN: # 아래방향키 엎드리기
                dino_down=True
            if (event.key==pygame.K_UP or event.key==pygame.K_SPACE) and not dino_jump: # 위방향키, 스페이스바 점프
                dino_jump=True
                dino_G=-18 # 공룡에게 적용되는 중력
                dino_img_idx=24
                dino_size=dino_img[dino_img_idx].get_rect().size
                dino_y_pos=160-dino_size[1]
        if event.type==pygame.KEYUP:
            dino_down=False

    # 배경 움직임
    background[0]["x_pos"]-=game_speed
    background[1]["x_pos"]-=game_speed
    if background[0]["x_pos"]==-480:
        background[0]["x_pos"]=480
    if background[1]["x_pos"]==-480:
        background[1]["x_pos"]=480

    # 공룡 위치와 이미지 결정
    if not dino_jump:
        dino_img_idx=(dino_img_idx+1)%12 # 걷는 모션
        if dino_down:
            dino_img_idx+=12 # 엎드렸을 때의 걷는 모션
        dino_size=dino_img[dino_img_idx].get_rect().size
        dino_y_pos=160-dino_size[1]
    else:
        dino_y_pos+=dino_G # 점프 시 중력값 번화
        dino_G+=2
        if dino_G>18:
            dino_jump=False # 착지 후 점프 종료

    # 장애물 생성 및 위치 결정
    for box_idx, box_val in enumerate(box):
        box[box_idx]["x_pos"]-=game_speed
        if box[box_idx]["x_pos"]<-100: # 이미 넘어간 장애물 삭제
            del box[box_idx]

    while len(box)<3: # 5개의 장애물 유지
        box.append(add_box(box,box_img))

    # 충돌 처리
    dino_rect=dino_img[dino_img_idx].get_rect() # 공룡 오브젝트 설정
    dino_rect.left=dino_x_pos
    dino_rect.top=dino_y_pos

    # 장애물과 충돌 처리
    for box_idx, box_val in enumerate(box):
        box_rect=box_val["img"].get_rect()
        box_rect.left=box_val["x_pos"]
        box_rect.top=box_val["y_pos"]
        
        if dino_rect.colliderect(box_rect) and box_val["x_pos"]>=0:
            run=False
            break

    # 화면 출력
    screen.blit(background[0]["img"],(background[0]["x_pos"],0))
    screen.blit(background[1]["img"],(background[1]["x_pos"],0))
    for box_idx, box_val in enumerate(box):
        screen.blit(box_val["img"],(box_val["x_pos"],box_val["y_pos"]))
    screen.blit(dino_img[dino_img_idx],(dino_x_pos,dino_y_pos))
    screen.blit(game_font.render("%05dm"%int(length/3),True,(0,0,0)),(400,10))

    pygame.display.update() # 화면 갱신
    length+=1

# 종료 후 화면 재출력
screen.blit(background[0]["img"],(background[0]["x_pos"],0))
screen.blit(background[1]["img"],(background[1]["x_pos"],0))
for box_idx, box_val in enumerate(box):
    screen.blit(box_val["img"],(box_val["x_pos"],box_val["y_pos"]))
screen.blit(dino_img[dino_img_idx],(dino_x_pos,dino_y_pos))
screen.blit(game_font.render("%05dm"%int(length/3),True,(0,0,0)),(400,10))

if dino_img_idx<12:
    screen.blit(dino_img[25],(dino_x_pos,dino_y_pos))
elif dino_img_idx<24:
    screen.blit(dino_img[26],(dino_x_pos,dino_y_pos))
else:
    screen.blit(dino_img[27],(dino_x_pos,dino_y_pos))

pygame.display.update()
pygame.time.delay(2000)

pygame.quit()