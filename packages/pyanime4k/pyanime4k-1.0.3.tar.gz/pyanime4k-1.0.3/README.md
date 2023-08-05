# pyanime4k
pyanime4k is a simply package to use anime4k in python, easy, fast and powerful.

# Usage
    import pyanime4k

    # Quickly show a image which be processed by anime4k
    pyanime4k.showImg2X("p1.png")
    # Convert images by anime4k
    pyanime4k.cvtImg2X("p1.png")
    pyanime4k.cvtImg2X(("p2.png","p3.png"),dstPath="./ouput")
    # Convert videos by anime4k
    pyanime4k.cvtVideo2X("p1.mp4")

    # Manually
    p = pyanime4k.Anime4K()
    # Image processing
    p.loadImage("p1.png")
    # Show the infomation of processing
    p.showInfo()
    # start processing
    p.process()
    # Preview result
    p.showImage()
    # Save image
    p.saveImage("p1_out.png")

    #Video
    p.loadVideo("p1.mp4")
    # Video need specify the output file name in advance
    p.setVideoSaveInfo("p1_out.mp4")
    p.showInfo()
    p.process()
    p.saveVideo()

See the [GitHub page](https://github.com/TianZerL/pyanime4k) of pyanime4k