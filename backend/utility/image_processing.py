import replicate
def generate_image(prompt, negative_prompt, guidance_scale=7.5, inference_steps=50,seed = 20):
    output = replicate.run(
        "cloneofsimo/realistic_vision_v1.3:db1c4227cbc7f985e335b2f0388cd6d3aa06d95087d6a71c5b3e07413738fa13",
        input={"prompt": prompt,
               "negative_prompt": negative_prompt,
               "num_inference_steps": inference_steps,
               "num_outputs": 3,
               "guidance_scale": guidance_scale,
               "width": 768,
               "height": 512,
               "seed":seed,
#               "safety_checker": False,
               },
    )
    return output

def generate_image_using_prompt(prompt):
    guidance_scale = 12
    inference_steps = 90
    seed =100
    #duration = "morning"
#     shot = "close-up shot"
    #prompt = f'landscape view, people strolling in the {city}, back side view, {duration}, {season}, {shot}, heavily detailed, movie shot, movie quality, hdr, 8k'
    prompt_gen = f'{prompt},heavily detailed, movie shot, movie quality, hdr, 8k'
    negative_prompt = """(short dresses),((bare body)),((backless cloth)),((sleevless cloth)),(fire on water),(fire on boat),(unreal locations),(unreal placement of items),(humans walking on water),(incomplete streets),(incomplete shoulder strap),(incomplete dress),(distorted eyes),(incomplete face),((duplicate faces),(duplicate building),(duplicate body),(duplicate structures)),(incomplete buildings),(incomplete structures),(incomplete hands),(incomplete items),(incomplete figures),(full body),((low detailed)),(duplicates), ((deformed face)),out of frame, lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, 
    ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, 
    bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, 
    long neck, username, watermark, signature,watermark, words, bad art, blurry, cropped, error, jpeg artifacts, low quality, lowres, normal quality, worst quality, ((futuristic)), 
    ((not detailed)), font, flyer text, ((text)), title, watermark, ((letters)), signature, username, words, (logo), ((badly drawn)), ((poor design)), deformed buildings, mutated buildings, ((unrealistic))"""
    url = generate_image(prompt_gen, negative_prompt, guidance_scale, inference_steps,seed)
    return url 
