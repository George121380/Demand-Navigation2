# !/usr/bin/env python
import requests
from datetime import datetime
current_time = datetime.now()
header = {
        "Content-Type":"application/json",
        "Authorization": "Bearer fa-YjAyODMwNjgtZDE3YS00MjU1LWIzZDQtZmNmOWFiNDQ0ZmUzMTY5NzUyODgzNjAx"
}

prompt="""You're a housekeeper. I need you to tell me what items in my room can help me to fulfill my demand. Note that my demands can always be seperated into two parts:<basic demand>,<preference>.\n My demands are:"""
prompt+=""" "I want to wash my dog, but I don't want to use soap." """

# 2. It's really hot today, I need to cool down, maybe an electric fan or air conditioner would be ideal.  
# 3. I want to entertain some friends over, I am thinking of something fun we could play indoors.
# 4. I am craving some homemade snacks, my oven and some baking ingredients would be perfect.
# 5. I need to get some work done, but I prefer working on a table with a comfortable chair.
# 6. I am feeling tired, and I want to rest. A comfortable bed or hammock would be ideal.
# 7. I am interested in capturing some memorable moments, a good quality camera will be fitting.
# 8. I want to go out but need some mode of transportation, my scooter or car could be useful.
# 9. I want to send some letters, so I'll need my writing materials and the postbox.
# 10. I would like to enjoy some music while relaxing on my easy chair, a music system or earphones would be fantastic.\n"""

# prompt+="""1. I am feeling a bit cold and would love to make myself warm, preferably something soft to cover with. 

# 2. I need to do some work, and I prefer a calmant, quiet and organized place to sit and concentrate.

# 3. I am hungry and want to cook something quick, I wish there was an easier way to heat the food. 

# 4. I feel like I should tidy up the house, but I don't know where to put all my stuff.

# 5. I want to enjoy a movie at home, I would definitely prefer to have some device to project it onto a big screen.

# 6. I am in the mood for some fun activity, probably some physical game that I can play indoors.

# 7. I need to relax for a bit, it would be nice to lay down somewhere comfortable and play soft music in the background.

# 8. I have been standing and working for long, wish there was some comfortable place to sit and unwind.

# 9. It's very hot today, I need something that can help in maintaining a cool ambiance.

# 10. I am having trouble getting to sleep, a soft, soothing sound, or music might help me sleep better."""

prompt+="""Above are my demands. And I have those items in my room:\nchina_cabinet, pinball_machine, storage_box, pond, scooter, blanket, earphone, pool_table, toilet_paper_holder, sugar_bowl, ball_chair, slide, fence, bath_mat, wall_hook, electric_fan, bag, faucet, toilet_brush, towel_rail, cup, dvd_player, sofa, camera, handle, trailer, magazine_rack, stove, headboard, blender, kitchen_timer, easy_chair, chaise_longue, window_curtain, chandelier, interior_barn_door, kitchen_scale, easel, wall_decor, armchair, soap_dispenser, spade, single_bed, doorbell, beanbag_chair, eames_chair, hammock, wall_unit, hand_glass, postbox, vase, notepad, trunk, toilet, hall_tree, swing_bench, window_blind, projector, board_game, doormat, knife, plush_toy, videodisk, window, cabinet, wreath, paper_organizer, spice_holder, bread-bin, oven, file, wall_mirror, candle, globe, soap, table_mirror, flower, air_conditioner, window_shade, table_runner, gazebo, letter, trampoline, towel, glass, paper_towel, coaster, paperweight, cellular_telephone, tapestry, throw, bunk_bed, microphone, clothes_dryer, ceiling_lamp, cooker, wall_clock, side_table, soda_can, folding_chair, chest_of_drawers, picnic_table, bedclothes, candelabrum, bridge, room_divider, hook, bed, car, audio_system, serving_cart, pet_bed, dog, elevator_door, drawer, wall_calendar, washer, flower_in_vase, wall_art, wine_bucket, surfboard, candle, wall_shelving, double_bed, place_setting, jar, cake_stand, butter_dish, dish_rack, toilet_bag, table_lamp, double_door, mousepad, subwoofer, picture_frame, monitor, pestle, toiletry, toilet_flush_plate, bottle_opener, lantern, blanket_chest, bathroom_scale, camcorder, fireplace, shoe_rack, christmas_stocking, radio_receiver, bookcase, streetlight, storage_bench, greenhouse, workbench, lamp, mattress, bucket, floor_mirror, socket, base_cabinet, foosball_table, roof, sculpture, sliding_door, whiteboard, chicken, chair, bag, picnic_rug, jewelry_box, telephone, hourglass, mirror, mat, smoke_detector, planter, candlestick, nightstand, person, napkin, curtain_rod, drawer_unit, television_receiver, roaster, bar, l-shaped_couch, dresser, punch_bowl, potholder, sink_cabinet, mantel_clock, coffee_table, ball, cage, laptop, wind_chime, track_lighting, timer, laundry_bag, pedestal_sink, cafeteria_tray, piggy_bank, plaything, cushion, string_lights, mixer, buffet, place_mat, book, soap_dish, sink, dishwasher, net, measuring_cup, basket, cabin, shoebox, cruet, credenza, wall_panel, garage_door, penguin, washer, vacuum, chopping_board, strainer, computer_screen, towel_rack, desk, table, trellis, mixing_bowl, sheep, daybed, game_table, floor_lamp, tissue_box, blackboard, toilet_paper_holder, cup, flat_bench, camp_chair, candlestick, binder, gate, rocking_chair, coffee_maker, grandfather_clock, hot_tub, bath_towel, drum_set, showerhead, playhouse, shot_glass, casserole, elevator, bathrobe, fire_extinguisher, kitchen_island, carafe, hobby, coffeepot, medicine_chest, dollhouse, mailbox, caddy, salver, screen, door, radiator, recliner, sink_stand, computer_work_area, shower_stall, fan, toaster_oven, exercise_bike, bandsaw, bar_stool, conference_table, watering_can, table-tennis_table, wall_organizer, wine_rack, magnet, toy_box, washbasin, book, dryer, sewing_machine, spoon, range_hood, refrigerator, console_table, cat, media_player, shower_door, skateboard, dining_area, wall_socket, beam, swing_chair, quilt, umbrella, colander, bi-fold_door, railing, highchair, shower_faucet, crib, barbecue, microwave, coffee_table, soccer_ball, end_table, motorcycle, bench, towel, football, cookie_sheet, bidet, heating_system, shower_caddy, wall_sign, urinal, purse, clock, bicycle, toilet_brush, tray, birdcage, ashtray, shed, switch, darts, saucepan, gym_equipment, wall_sticker, cake, playhouse, printer, electric_frying_pan, desk_organizer, bolster, christmas_tree, horse, switch, chest_of_drawers, armrest, handcart, video_game_console, greeting_card, frying_pan, pan, bar_stool, pitcher, telescope, cake, drawer_unit, tent, barrow, wall_hook_rack, ceiling_lamp, chess, toilet_paper_holder, wine_bottle, hanging_cabinet, bookend, firepit, toilet_tissue, wardrobe, pepper_mill, revolving_door, stool, wall_shelf, hook, club_chair, round_daybed, valve, kitchen_cabinet, potted_plant, punching_bag, chest, sauna, wok, tablet_computer, weight, throw_pillow, playpen, umbrella_stand, kettle, piano, shower_curtain, plate, cradle, countertop, tv_stand, grab_bar, pet_bowl, magazine, toaster, desk_calendar, bouquet, music_stand, plant_stand, dining_table, air_hockey_table, drum, mantel, swivel_chair, ceiling_fan, ironing_board, hedge, stove, drying_rack, water_scooter, bottle, towel_ring, reamer, mobile, broom, makeup_mirror, wineglass, bulletin_board, poster, bathtub, towel_ring, toiletry, king_bed, step_ladder, chain_saw, hatbox, shoe, board_game, ladder, radio_receiver, spicemill, shoe_rack, spice_rack, guitar, hanging_cabinet, lawn_mower, aquarium, clothing_rack, pendant_lamp, cocktail_shaker, ottoman, clothes_tree, power_saw, swimming_pool, shopping_bag, thermos, rack, dressing_table, washbasin, footstool, loudspeaker, ashcan, shower_pan, wall_art, balcony, toilet_brush, record_player, kitchen_appliance, bicycle_rack, plant, pet_house, tureen, toiletry, mantel_clock, seat_cushion, step_stool, stairway, WordNet, Synset, Key, notebook, wall_lamp, jug, alarm_clock, canister, swivel_chair, luggage_rack, pathway_light, utensil, swing, tree, crate, towel_rack, coatrack, lectern, curtain, rock, bowl, shelving, bench_grinder, candle, spectacles, treadmill, mat, straight_chair, knocker, swing, tumbler, espresso_maker, overnighter, towel_rack, dartboard, hand_glass, kitchen_appliance, teapot, rug, birdhouse, hamper, armoire, play_area, mixer, ladder_bookcase, gift_box, safe, bathtub, parrot.\n"""

prompt+="""Tell me what items in my room are helpful to fulfill my basic demands and what items can probably fulfill my preference.\n"""

prompt+="""You should know that sometimes a demand can be met by finding just one item that meets the requirements, and sometimes my demand require several items to work in conjunction with each other to meet it."""

# format1="""The format is like this:n.basic demand:<basic demand>\nnormal items:<normal item1>, <normal item2>,...<normal itemn>.\npreference:<preference>\nprefered items:<prefered item1>,<prefered item2>,...<prefered itemn>\n\n"""我自己设计的format

format1="""Please output a json file in this format:
{
    task_instruction: $basic_demand$, $preference$
    basic_demand: xxx
    preference: xxx
    basic_object:[a,b],[a,c],[d],[a,f,g]
    preference_object:[a,b],[d]
}

Here is an example:
{
  "task_instruction": "I want to listen to music, but I don't want the sound to disturb my family.",
  "basic_demand": "Listen to music",
  "preference": "Not disturb family with music sound",
  "basic_object": [["audio_system"], ["radio_receiver"], ["record_player"], ["loudspeaker"], ["media_player"], ["headphone","media_player"],["laptop"],["laptop","headphone"], ["tablet_computer"],["tablet_computer","headphone"], ["cellular_telephone"],["headphone","cellular_telephone"]],
  "preference_object": [["headphone","cellular_telephone"], ["tablet_computer","headphone"],["tablet_computer","headphone"]]
}
"""

format2="""The format is like this:n.<basic demand>:<normal item1>, <normal item2>,...<normal itemn>.\n<preference>:<prefered item1>,<prefered item2>,...<prefered itemn>\n\n"""

format_origin="""Tell me what items in my room can probably fulfill my basic demands and what items can probably fulfill my preference.\n The format is like this:n.<basic demand>: <normal item1>, <normal item2>,...<normal itemn>.\n<preference>:<prefered item1>,<prefered item2>,...<prefered itemn>\n"""


prompt+=format1#选择format

example_explain="""Above is the format of the answer. In the "basic_demand" you need to summarize and distill my basic demand.  And in the "basic_object" you need to list all the items combinations that are related to my demand or can probably fulfill my basic demand. In the "preference" you need to summarize and distill my preference. And in the "preference_object" you need to list all the items combinations in the "basic_object" that can probably fulfill my preference. Noted that can "preference_object" only be a subset of "basic_object"! You need to think of the elements needed to fulfill a need and for each element, find a corresponding item!\n"""

prompt+=example_explain

prompt+="""Try to list all the possible items for each demand."""


post_dict = {
        "model": "gpt-4-0613",
        "messages": [{
                "role": "user",
                "content": prompt
    }]
}

r = requests.post("https://frostsnowjh.com/v1/chat/completions", json=post_dict, headers=header)
response_content = r.json()

with open("hard.txt", "a") as file:
        
        file.write(str(current_time) + "\n")
        file.write(response_content['choices'][0]['message']['content'] + "\n"+ "\n")
