Intro 

## Using this website

### Are you storing my images?

No. I don't store any of your images. Not the ones you upload, nor the ones you generate. This is a static website, where all conversions happen in-browser by using Javascript.

### Can I use the images I generate commercially?

Yes, you can do whatever you want with them. You really don't have to, but I would be grateful if you mention my site somehow.

### How do I change the output?

Once you have uploaded an image, a controls panel should appear at the bottom of your screen. Here you can define your desired output pixel dimensions. You can also use a quick control to simply use the aspect ratio of the uploaded image.

The first time you upload an image, the output format is as close to the uploaded image. For example, if your uploaded image has an aspect ratio of 4:3 (width:height) then the output also has this aspect ratio. You can edit this via the controls panel.

### How can I download the generated pixel art?

Once you are happy with the generated pixel art, just press the appropriate SVG or PNG button (right below the image). The download should start immediately.

SVG is a scalable vector graphics file. This is a file that you can scale or resize, without losing quality. Perfect for printing on a large canvas, a t-shirt, etc. If you prefer to have a regular image, or want both, then you can also download the PNG image version.

The filename is similar to the filename of the uploaded image, with a suffix added that contains some information about the chosen output format. This way you can easily distinguish between several generated versions of the same uploaded image.

## Creation of this website

### Who created this website?

Just me, Tristan. You can connect with me on <a href="https://www.linkedin.com/in/tristanbains/">LinkedIn</a>.

### Why did you create this website?

I wanted to build a simple website for my data science portfolio. Read more on the development and tech stack used in the <a href="{{url_for('page',path='about')}}">about section</a>.

### How are the pixelated images created?

For instance, suppose your uploaded image is 600x800 (width x height) and you want a 30x30 pixelated output.

Then the first step is to carve out a center cropped 600x600 square (the biggest multiple of 30x30 inside the uploaded image).

In the next conv2d layer this 600x600 is divided into 20x20 squares (because 600/30=20). For every 20x20 square, we calculate the average color, which is "just" the average of all 400 rgb values.

All these calculations happen in a couple of lines of tensorflow.js code. After that these so-called tensors are converted to svg strings, and later on svg files and png files. All this happens in-browser.

### The pixelated output is "blurry"?

This is a consequence of the way the pixels are calculated, namely averaging.

For example, suppose your image has an area that is half black, half white. Then the calculated pixel color for that area will be its average, i.e. gray. This happens to every area that contains multiple colors.

I have experimented with other methods than just averaging. One was calculating the min, max and average. The average has the role of deciding whether to take the min or the max (so the average itself is never used for generating the output). If the max was closer to the average then take the max, if the min was closer to the average then take the min. This results in a sharper output, but only looked better for uploaded images with low detail levels. In most cases the average looks a lot better.