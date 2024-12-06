title: Generating Pixel Art from any uploaded image with Tensorflow.js
subtitle: And lots of vanilla Javascript...
description: Information on how and why I built PixelatedArtwork.com. My learnings, what tech stack was used.

Hi! I'm Tristan Bains, a Dutch data scientist from the Amsterdam area in the Netherlands.

I wanted to add a fun, end-to-end project to my data science portfolio. I also wanted to use TensorFlow.js, the JavaScript version of TensorFlow, which I hadn't used before. While I had previous experience with TensorFlow's Python version, I was new to its JavaScript counterpart.

I considered many ideas but ultimately chose to create a project that converts user-uploaded images into pixel art. To build this quickly, I decided to use tools I already knew: Python Flask and TailwindCSS. This way, the only new thing I had to learn was TensorFlow.js.

Looking back, while I gained valuable experience working with TensorFlow.js, I spent most of my time designing a user-friendly experience. You can read more about my reflections at the bottom of the page.

<h2>Table of contents</h2>

[TOC]

## Upfront requirements

Before starting, I wanted to ensure that the project met a few key requirements:

* **User-friendly**: The user experience (UX) should be self-explanatory, and look good. The image generation should be fast (i.e. *low latency*).
* **Quick development**: I used familiar tools like Python Flask, TailwindCSS, and JavaScript to speed up the process.
* **Easy deployment**: I opted for a static website with JavaScript handling the image processing. This makes hosting simple and cheap.

## User Interaction and Code Flow

TOnce you load the homepage, here's what happens:

1. **Image Upload**: You upload an image of your choice.
2. **Pixelation**: A JavaScript listener activates TensorFlow.js, which creates multiple pixelated versions of your image. These pixelated images are stored as SVG strings in your browser's memory.
3. **Display and Variation**: The pixelated images are displayed as different image formats, such as Lego-style, circular, and square grid.
4. **User Controls**: Once the initial images are displayed, you can adjust them using various controls. The user controls become visible at the bottom of the page
5. **Further Interaction**: You can continue to interact with the website by uploading new images, editing existing ones, or downloading the generated images.

## Tech stack

### Front-end

* **Tailwind CSS**: I use this CSS framework in all of my Python Flask HTML template files. It is a very intuitive CSS framework to define all css by simply adding classes to HTML tags.
* **DaisyUI**: Built on top of Tailwind CSS, DaisyUI provides pre-built components. The component I used most was the carousel.
* **Tensorflow.js**: This JavaScript version of TensorFlow is used for image processing and pixelation.
* **Javascript**: I used JavaScript to make the website interactive. For example, when you upload a file or change the output size, JavaScript triggers the necessary calculations.

### Back-end

While the website appears dynamic, it's actually a static web application, eliminating the need for a traditional database.

* **Python Flask**: Flask is the framework used to create a web app. My implementation uses routes for the main page, the inspiration pages, the FAQ page and Markdown-based pages.
* **Flask-Markdown**: Used for writing this page, the about page. It converts a Markdown text file into HTML.
* **Flask FlatPages**: At the end of the development, I run a build command to turn the web app into a static website.

### Other

* **Microsoft Visual Studio Code**: My preferred code editor for writing all the code (Python, Javascript, Markdown).
* **Docker**: I used Docker to containerize my web application, making it easier to set up and run locally.
* **Cloudflare Pages**: This is where this sets gets hosted. The Github repo that contains the static website files is connected to CloudFlare Pages.

## Reflections on the project

### The deep learning aspect

Initially, I was excited to dive into deep learning with TensorFlow.js. However, the core deep learning component ended up being quite straightforward. It primarily involved slicing the uploaded image and applying a simple 2D convolutional layer. I spent more time optimizing the browser's memory management for tensor operations than on the actual model architecture.

### User experience

The most time-consuming part of the project was refining the user experience. Early versions were confusing, requiring numerous info boxes to guide users.

To improve this, I adopted a minimalist approach, removing unnecessary options and streamlining the workflow. I also implemented lots of JavaScript listeners to make user interactions more intuitive and responsive. Because of this, I picked up a lot of JavaScript.

### Front-end

A few months ago, I learned about DaisyUI. I liked it so much that I decided to use it for this project. It made building the website even faster than using just TailwindCSS.

I hope you like the project. Feel free to <a href="https://www.linkedin.com/in/tristanbains/">contact me</a> anytime.

Tristan