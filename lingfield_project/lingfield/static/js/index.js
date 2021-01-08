

// function pageTransition() {
//     var tl = gsap.timeline();
//     tl.to(".loading-screen", {duration: 1.2, height: "100%", bottom: "0%",ease: "Expo.easeInOut",});

//     tl.to(".loading-screen", {duration: 1, height: "100%", bottom: "100%",ease: "Expo.easeInOut",delay: 0.3,});
//     tl.set(".loading-screen", { bottom: "-100%" });
// }

// function contentAnimation() {
//     var tl = gsap.timeline();
//     tl.from(".animate-this", { duration: 1, y: 30, opacity: 0, stagger: 0.4, delay: 0.2 });
// }

// function delay(n) {
//     n = n || 2000;
//     return new Promise((done) => {
//         setTimeout(() => {
//             done();
//         }, n);
//     });
// }


//     barba.init({
//         sync: true,

//         transitions: [
//             {
//                 async leave(data) {
//                     const done = this.async();

//                     pageTransition();
//                     await delay(1000);
//                     done();
//                 },

//                 async enter(data) {
//                     contentAnimation();
//                 },

//                 async once(data) {
//                     contentAnimation();
//                 },
//             },
//         ],
//     });


// // -----------------------------------------------------------------------    MAIN   ---------------------------------------------------------------/
// function pageTransition() {
//     let tl = gsap.timeline();
//     tl.to('ul.transition li', { duration: .5, scaleY: 1, transformOrigin: "bottom left", stagger: .2});
//     tl.to('ul.transition li', { duration: .5, scaleY: 0, transformOrigin: "bottom left", stagger: .1, delay:.1,});
// }
// // function contentAnimation() {
// //     let tl = gsap.timeline();
// //     tl.from('.left', { duration: 1.5, translateY: 50, opacity: 0 });
// //     tl.to('img', { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0% 100% )" },  "-=1.1")
// // }


// function delay(n) {
//     n = n || 1000;
//     return new Promise(done => {
//         setTimeout(() => {
//             done();
//         }, n);
//     });
// }

//     barba.init({

//         sync: true,

//         transitions: [{

//             async leave(data) {

//                 const done = this.async();

//                 pageTransition();
//                 await delay(1000);
//                 done();

//             },

//             async enter(data) {
//                 contentAnimation();
                
//             },

//             async once(data) {
//                 contentAnimation();
//             }

//         }]
//     });

