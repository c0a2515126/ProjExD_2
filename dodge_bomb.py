import os
import random #練習問題２
import sys
import time#演習課題１
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool,bool]:#ここから練習問題３


    """
    引数：こうかとん又は爆弾のrect
    戻り値：タプル（縦横判定結果）
    画面内ならtuue,画面外ならfalse
    """

    yoko, tate = True , True
    if rect.left < 0 or WIDTH < rect.right:
        yoko =False
    if rect.top < 0 or HEIGHT <rect.bottom:
        tate = False
    return yoko, tate#ここまで練習問題３


def gameover(screen: pg.Surface) -> None:#ここから演習１


    """
    爆弾着弾時に画面をブラックアウトし
    泣いているこうかとんとgeme overの文字を5秒間表示する関数
    引数：screen(画面surface)
    """
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.fill((0, 0, 0))
    black_sfc.set_alpha(160) 

    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2

    cry_img = pg.image.load("fig/8.png")
    cry_rct1 = cry_img.get_rect()
    cry_rct2 = cry_img.get_rect()
    cry_rct1.center = txt_rct.left - 50, HEIGHT // 2
    cry_rct2.center = txt_rct.right + 50, HEIGHT // 2

    black_sfc.blit(txt, txt_rct)
    black_sfc.blit(cry_img, cry_rct1)
    black_sfc.blit(cry_img, cry_rct2)

    screen.blit(black_sfc,[0,0])
    pg.display.update()
    time.sleep(5)#ここまで演習１


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:#演習２完了


    """
    移動量の合計タプルに応じたこうかとんSurfaceの辞書を生成する関数
    戻り値：{(移動量x, 移動量y): 画像Surface} の辞書
    """
    kk_img_l = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img_r = pg.transform.flip(kk_img_l, True, False)

    return {
        (0, 0): kk_img_l,
        (+5, 0): kk_img_r,
        (+5, -5): pg.transform.rotozoom(kk_img_r, 45, 1.0),
        (0, -5): pg.transform.rotozoom(kk_img_r, 90, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img_l, -45, 1.0),
        (-5, 0): kk_img_l,
        (-5, +5): pg.transform.rotozoom(kk_img_l, 45, 1.0),
        (0, +5): pg.transform.rotozoom(kk_img_r, -90, 1.0),
        (+5, +5): pg.transform.rotozoom(kk_img_r, -45, 1.0),
    }#演習２完了

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}# 練習問題１


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_imgs = get_kk_imgs() 
    kk_img = kk_imgs[(0, 0)] 
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img=pg.Surface((20, 20))#練習問題２
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)#練習問題２
    bb_img.set_colorkey((0, 0, 0))#練習問題２
    bb_rct = bb_img.get_rect()#練習問題２
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)#練習問題２
    vx, vy = +5, +5#練習問題２

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():#練習問題１
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True, True):#練習問題３
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])#練習問題３
        kk_img = kk_imgs[tuple(sum_mv)] 
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)#練習問題２
        yoko, tate = check_bound(bb_rct)#ここから練習問題３
        if not yoko:
            vx *= -1
        if not tate:
            vy *=-1#ここまで練習問題３
        screen.blit(bb_img, bb_rct)#練習問題２
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()#ok
