import pygame

from py2dgame import CoreStage, CoreSprite

RET_ERROR = None
RET_OK = True
RET_WARN = False

stage = None

def create_sprite(costume="default"):
    global stage
    return CoreSprite(stage, costume)

def create_stage(force=False):
    global stage
    if stage:
        if force:
            stage = CoreStage()
        else:
            print("Error: already stage created")
            exit(1)
    else:
        stage = CoreStage()
    
    return stage

def stop_stage():
    global stage
    stage.running = False
    stage.message_broker.mark_completed()
    
    stage.sprites.empty()
    stage.visible_sprites.empty()
    
    stage.bubbles.empty()
    stage.visible_bubbles.empty()
    stage.monitor_group.empty()


def mouse(): ## mouse loc
    x = pygame.mouse.get_pos()[0]
    #sx = ((x - stage.offset_x) / stage.scale_factor) - stage.width / 2
    y = pygame.mouse.get_pos()[1]
    #sy = -(y - stage.offset_y) / stage.scale_factor + stage.height / 2

    clicked = any(pygame.mouse.get_pressed())
    return x, y, clicked

def pos_in_rect(x, y, left, top, width, height):
    if (x > left and x < left +  width) \
            and (y > top and y < top + height):
        #print("OK")
        return True
    return False

def touching_pointer(sprite): ## touch mouse
    x, y, clicked = mouse()

    #print(x , sprite.rect.left, sprite.rect.left -  sprite.rect.width)
    #print(y ,sprite.rect.top ,sprite.rect.top - sprite.rect.height)
    rect = sprite.rect
    if pos_in_rect(x, y, rect.left, rect.top, rect.width, rect.height):
        #print("OK")
        return True
    return False

def touching_clicked_pointer(sprite): ## touch and click mouse
    x, y, clicked = mouse()
    rect = sprite.rect
    #if clicked:
    #    print(sprite)
    #    print(x , sprite.rect.left, sprite.rect.left,  sprite.rect.width)
    #    print(y ,sprite.rect.top, sprite.rect.top , sprite.rect.height)
    if (clicked) and  pos_in_rect(x, y, rect.left, rect.top, rect.width, rect.height):
        #print("OK")
        #print("OK")
        return True
    return False

def touching_color(color, threshold=0): ## touch color
    x, y, clicked = mouse()

    c = stage.surface.get_at((x, y))[:3]
    #print("color=", c)
    touch = True
    for i in [0, 1, 2]:
        if abs (color[i] - c[i]) > threshold:
            touch = False
            break

    print("touch", touch)
    return touch


def is_touched(sprite, sprites): ## touch sprite on sprite
    touch = False
    for d in sprites:
        if sprite.sensing_touchingobject_sprite(d):
            touch = True
            break
    return touch

def start_sound_deperecated(sprite, name, block=True, loop=0): ## sound play
    #sound = sprite.sound_manager.get_sound(name)
    #print("TESTTEST: sound=", sound)

    try:
        #print(f"starting sound {name} on sprite {sprite}")
        if block:
            sprite.sound_playuntildone(name)
        else:
            ret = sprite.sound_play(name, loop=loop)
            #print("TESTTEST: sound play ret=", ret)
        return RET_OK
    except AttributeError as e:
        print(f"sound {name} error on sprite {sprite}", e)

    return RET_ERROR

def start_sound(sprite, name, block=True, loop=0): ## sound play
    channel = sprite.data_variable("channel")
    #print("channel=", channel, channel.get_busy(), channel.get_volume())

    sound = sprite.sound_manager.get_sound(name)
    #print(name, sound)
    if sound is None:
        return RET_ERROR

    if channel.get_busy():
        print(f"channel is bussy for starting sound {name} on sprite {sprite}")
        return RET_WARN

    try:
        print(f"starting sound {name} on sprite {sprite}")
        if block:
            channel.play(sound, 0)
            sprite.code_manager.current_block.add_to_wait_time = sound.get_length()
        else:
            if sound is not None:
                channel.play(sound, loop)
            return channel

    except AttributeError as e:
        print(f"sound {name} error on sprite {sprite}", e)
        return RET_ERROR


    return RET_ERROR


