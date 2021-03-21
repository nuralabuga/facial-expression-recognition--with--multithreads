# facial-expression-recognition--with--multithreads

This site was built using [piyush2896
/
Facial-Expression-Recognition-Challenge](https://github.com/piyush2896/Facial-Expression-Recognition-Challenge).

######It was worked on camera.py file in the folder and updated to camera_multithread_ram.py. The code has been turned into a multi-thread running on separate threads. ProducerThread reads the video and buffers the frames, while ConsumerThread predicted with the pre-trained model given in the project.

######The code works in real-time and attention has been paid to memory usage. It has been arranged in a way to profile the memory usage while the code is running.

######I saw that the buffer size increased up to 700 for a period of 30 seconds when I processed all the frames without any skipping while taking my frames on ConsumeThread, and the buffer size increased as the video duration increased. After that, I skipped the 5 frames I had determined, without processing them, and kept the buffer size stable in the 1-5 range. In this way, even if the video duration was longer, the ram was not swollen. (You can see it with the logs I put in the code.).



