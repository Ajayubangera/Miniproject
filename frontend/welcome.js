// =====================================
// Smooth Scroll for Navbar Links
// =====================================

document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault();

        const targetId = link.getAttribute("href").substring(1);
        const target = document.getElementById(targetId);
        const headerHeight = document.querySelector(".header").offsetHeight;

        if (target) {
            window.scrollTo({
                top: target.offsetTop - headerHeight - 20,
                behavior: "smooth"
            });
        }
    });
});


// =====================================
// Scroll to Top When Logo is Clicked
// =====================================

document.getElementById("logoBtn").addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});


// =====================================
// ⭐ Hero Get Started → Redirect to index.html
// =====================================

document.getElementById("heroGetStarted")?.addEventListener("click", () => {
    document.body.style.transition = "opacity 0.4s";
    document.body.style.opacity = "0";

    setTimeout(() => {
        window.location.href = "index.html";
    }, 400);
});


// =====================================
// ⭐ Header Get Started → Redirect to index.html
// =====================================

document.getElementById("headerGetStarted")?.addEventListener("click", () => {
    document.body.style.transition = "opacity 0.4s";
    document.body.style.opacity = "0";

    setTimeout(() => {
        window.location.href = "index.html";
    }, 400);
});


// =====================================
// Fake 3D Model Loader (Placeholder)
// =====================================

const faceContainer = document.getElementById("face3DContainer");

function loadFake3DModel() {
    const loadingText = document.querySelector(".loading-3d");

    setTimeout(() => {
        loadingText.style.opacity = "0";

        setTimeout(() => {
            loadingText.remove();

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

            renderer.setSize(300, 300);
            faceContainer.appendChild(renderer.domElement);

            const geometry = new THREE.SphereGeometry(1, 32, 32);
            const material = new THREE.MeshStandardMaterial({
                color: 0x00f3ff,
                metalness: 0.7,
                roughness: 0.2
            });

            const sphere = new THREE.Mesh(geometry, material);
            scene.add(sphere);

            const light = new THREE.PointLight(0xffffff, 2);
            light.position.set(5, 5, 5);
            scene.add(light);

            camera.position.z = 3;

            function animate() {
                requestAnimationFrame(animate);
                sphere.rotation.y += 0.01;
                sphere.rotation.x += 0.005;
                renderer.render(scene, camera);
            }

            animate();
        }, 300);
    }, 1500);
}


// =====================================
// GSAP Animations
// =====================================

gsap.from(".hero-title", {
    y: 40,
    opacity: 0,
    duration: 1,
    ease: "power3.out"
});

gsap.from(".hero-description", {
    y: 20,
    opacity: 0,
    duration: 1,
    delay: 0.3,
    ease: "power3.out"
});

// About Cards
gsap.utils.toArray(".about-card").forEach((card, index) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: "top 85%"
        },
        y: 50,
        opacity: 0,
        duration: 0.7,
        delay: index * 0.2,
        ease: "power3.out"
    });
});

// Team Cards
gsap.utils.toArray(".team-card").forEach(card => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: "top 80%"
        },
        y: 60,
        opacity: 0,
        duration: 0.8,
        ease: "power3.out"
    });
});


// =====================================
// Header Get Started Visibility
// =====================================

const headerGetStarted = document.getElementById("headerGetStarted");

window.addEventListener("scroll", () => {
    const heroBottom = document.querySelector(".hero-section").offsetHeight;

    if (window.scrollY > heroBottom - 400) {
        headerGetStarted.classList.add("show");
    } else {
        headerGetStarted.classList.remove("show");
    }
});


// =====================================
// Hide Header Button When Hero Button Visible
// =====================================

const heroBtn = document.getElementById("heroGetStarted");

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting)
            headerGetStarted.classList.remove("show");
        else
            headerGetStarted.classList.add("show");
    });
}, { threshold: 0.1 });

observer.observe(heroBtn);
