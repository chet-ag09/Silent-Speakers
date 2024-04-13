<h1>💡 Inspiration 💡</h1>
Few days ago, I was looking out of my bedroom window when I saw a deaf or hard of hearing person signing to their companion. I could feel that they were angry and the hearing person could not understand. At that moment, I thought about how I could make people understand sign while being accessible to all. That's how Silent Speakers App was born.

<h1>🤔 What it does 🤔</h1>
Silent Speakers is a sign language translation app designed to bridge the communication gap between the deaf and hearing communities. It allows users to:

Translate Sign Language to Text: Users can either hold up their hand and perform a sign in front of the app's camera, or upload an video of a sign. The app uses hand pose detection technology to identify the key features of the hand and translates it into the corresponding text.
View Sign Meanings: The app displays the text translation of the recognized sign, allowing users to understand the meaning conveyed through sign language.
Text-to-Sign Translation: Enabling users to type a word or phrase and see the corresponding sign language image on the screen.
The app provides two-way communication between the deaf and the non-deaf

<h1>🧐 How we built it 🧐</h1>
Silent Speakers utilizes MediaPipe's pre-trained hand pose detection model. This powerful tool allows the app to identify hand landmarks (fingertips, wrist, etc.) in real-time video frames captured from the device's camera. I used OpenCV for processing tasks like frame capture and Tkinter for the UI.

<h1>🚨 Challenges we ran into 🚨</h1>
The Challenges I ran into were making the app detect sign properly. I had to set proper and accurate threshold for the app to detect the sign gesture. Moreover, I had to learn the ASL signs to properly integrate it into my app.

<h1>🎯 Accomplishments that we're proud of 🎯</h1>
Accomplishments that I'm proud of are making the app accurately detect signs. Furthermore, I'm proud of making the sign detector and the UI work together. ;)

<h1>🎓 What we learned 🎓</h1>
I learned basics of ASL and I learned how to use tkinter to make the app's UI.

<h1>🔮 What's next for Silent Speakers 🔮</h1>
To make the Silent Speakers App even better, instead of detecting ASL, it will also detect different languages like BSL or ISL. This could make the app accessible to a wider audience which could bring us closer to eradicating the language barrier. The app could also have a ML model with wider data set for more accurate translation.
