/**
 * ProDig Hero Particle System
 * Implementación de "Materia Programable" con Three.js y HTML5 Canvas
 * 
 * Requisitos: Three.js (importado en el HTML)
 */

class ProgrammableMatter {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) throw new Error(`Contenedor ${containerId} no encontrado.`);

        this.PARTICLE_COUNT = 6000;
        this.particlesData = [];
        this.state = 'INITIAL'; // INITIAL, DISTORT_P, SCATTER, SERVICE, BACKGROUND
        
        this.initScene();
        this.initCanvasTextReader();
        this.createParticles();
        
        window.addEventListener('resize', this.onResize.bind(this));
        
        // Iniciar bucle de renderizado
        this.animate();

        // Secuencia automática de demostración
        setTimeout(() => this.triggerSequence(), 3000);
    }

    initScene() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
        this.camera.position.z = 250;
        
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.container.appendChild(this.renderer.domElement);
    }

    /**
     * Utiliza un Canvas 2D en memoria para dibujar texto y extraer
     * las coordenadas de los píxeles (X, Y) mapeadas al espacio 3D.
     */
    getTextCoordinates(text, fontSize = 60, width = 800, height = 200, yOffset = 0) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        canvas.width = width;
        canvas.height = height;
        
        // Fondo negro
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, width, height);
        
        // Texto blanco
        ctx.font = `bold ${fontSize}px "Inter", sans-serif`;
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, width / 2, height / 2);
        
        const imageData = ctx.getImageData(0, 0, width, height).data;
        const coords = [];
        
        // Escaneo de píxeles (saltamos algunos para optimización)
        for(let y = 0; y < height; y += 2) {
            for(let x = 0; x < width; x += 2) {
                const alpha = imageData[(y * width + x) * 4]; // Canal rojo es suficiente por ser B/N
                if(alpha > 128) {
                    coords.push({
                        x: (x - width / 2) * 0.4,
                        y: -(y - height / 2) * 0.4 + yOffset, // Invertir Y para Three.js
                        z: 0
                    });
                }
            }
        }
        return coords;
    }

    createParticles() {
        this.geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(this.PARTICLE_COUNT * 3);
        const targets = new Float32Array(this.PARTICLE_COUNT * 3);
        const originals = new Float32Array(this.PARTICLE_COUNT * 3);
        
        // Leer píxeles del texto principal
        const mainTextCoords = this.getTextCoordinates("Prospectiva Digital", 65);
        
        for(let i = 0; i < this.PARTICLE_COUNT; i++) {
            // Asignar una coordenada (reciclamos si hay más partículas que píxeles)
            const coord = mainTextCoords[i % mainTextCoords.length];
            
            // Ruido para darle grosor a la letra
            const noiseX = (Math.random() - 0.5) * 1.5;
            const noiseY = (Math.random() - 0.5) * 1.5;
            const noiseZ = (Math.random() - 0.5) * 4;
            
            const x = coord.x + noiseX;
            const y = coord.y + noiseY;
            const z = coord.z + noiseZ;
            
            // Posición inicial: Explosión aleatoria para efecto de entrada
            positions[i*3] = (Math.random() - 0.5) * 1000;
            positions[i*3+1] = (Math.random() - 0.5) * 1000;
            positions[i*3+2] = Math.random() * 500 - 250;
            
            targets[i*3] = x;
            targets[i*3+1] = y;
            targets[i*3+2] = z;
            
            originals[i*3] = x;
            originals[i*3+1] = y;
            originals[i*3+2] = z;
            
            // Lógica sencilla para separar las partículas que forman la letra "P"
            // (La P de Prospectiva está al extremo izquierdo del canvas)
            const isLetterP = x < -125 && x > -160;

            this.particlesData.push({
                isP: isLetterP,
                lerpSpeed: 0.02 + Math.random() * 0.05,
                noiseOffset: Math.random() * Math.PI * 2
            });
        }
        
        this.geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        this.geometry.setAttribute('target', new THREE.BufferAttribute(targets, 3));
        this.geometry.setAttribute('original', new THREE.BufferAttribute(originals, 3));
        
        // Material de alto rendimiento con Additive Blending
        const material = new THREE.PointsMaterial({
            color: 0x9d4edd, // Color púrpura ProDig
            size: 1.5,
            sizeAttenuation: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });
        
        this.points = new THREE.Points(this.geometry, material);
        this.scene.add(this.points);
    }

    triggerSequence() {
        const targets = this.geometry.attributes.target.array;
        const originals = this.geometry.attributes.original.array;
        
        // 1. ESTADO DISTORSIÓN DE LA 'P'
        this.state = 'DISTORT_P';
        for(let i = 0; i < this.PARTICLE_COUNT; i++) {
            if(this.particlesData[i].isP) {
                // Impulso hacia arriba y hacia adelante
                targets[i*3+1] += 40;
                targets[i*3+2] += 50;
                this.particlesData[i].lerpSpeed = 0.08; // Rápido
            }
        }

        // 2. ESTADO ESTALLIDO (SCATTER)
        setTimeout(() => {
            this.state = 'SCATTER';
            for(let i = 0; i < this.PARTICLE_COUNT; i++) {
                if(this.particlesData[i].isP) {
                    targets[i*3] += (Math.random() - 0.5) * 100;
                    targets[i*3+1] += (Math.random() - 0.5) * 100;
                    targets[i*3+2] += (Math.random() - 0.5) * 100;
                    this.particlesData[i].lerpSpeed = 0.04;
                }
            }
        }, 600);

        // 3. ESTADO SERVICIO (MORPHING)
        setTimeout(() => {
            this.state = 'SERVICE';
            const serviceCoords = this.getTextCoordinates("Páginas web con IA", 30, 800, 200, -50); // yOffset para ir abajo
            
            for(let i = 0; i < this.PARTICLE_COUNT; i++) {
                if(this.particlesData[i].isP) {
                    const coord = serviceCoords[i % serviceCoords.length];
                    targets[i*3] = coord.x + (Math.random() - 0.5);
                    targets[i*3+1] = coord.y + (Math.random() - 0.5);
                    targets[i*3+2] = coord.z + (Math.random() - 0.5) * 2;
                    this.particlesData[i].lerpSpeed = 0.05 + Math.random() * 0.03;
                }
            }
        }, 1500);

        // 4. ESTADO FONDO FLOTANTE Y RECUPERACIÓN DE LA 'P'
        setTimeout(() => {
            this.state = 'BACKGROUND';
            for(let i = 0; i < this.PARTICLE_COUNT; i++) {
                if(this.particlesData[i].isP) {
                    if(Math.random() > 0.4) {
                        // El 60% de las partículas regresan a formar la 'P' original
                        targets[i*3] = originals[i*3];
                        targets[i*3+1] = originals[i*3+1];
                        targets[i*3+2] = originals[i*3+2];
                        this.particlesData[i].lerpSpeed = 0.02;
                    } else {
                        // El 40% se va al fondo flotante (Ruido ambiente)
                        targets[i*3] = (Math.random() - 0.5) * window.innerWidth;
                        targets[i*3+1] = (Math.random() - 0.5) * window.innerHeight;
                        targets[i*3+2] = -200 - Math.random() * 300; // Al fondo
                        this.particlesData[i].lerpSpeed = 0.01;
                    }
                }
            }
        }, 5000);
    }

    onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        
        const positions = this.geometry.attributes.position.array;
        const targets = this.geometry.attributes.target.array;
        const time = Date.now() * 0.001;

        for(let i = 0; i < this.PARTICLE_COUNT; i++) {
            const data = this.particlesData[i];
            
            // Interpolación Lineal (Lerp) de Posición Actual a Objetivo
            positions[i*3] += (targets[i*3] - positions[i*3]) * data.lerpSpeed;
            positions[i*3+1] += (targets[i*3+1] - positions[i*3+1]) * data.lerpSpeed;
            positions[i*3+2] += (targets[i*3+2] - positions[i*3+2]) * data.lerpSpeed;

            // Micro-movimiento para efecto orgánico de materia
            if (this.state === 'BACKGROUND' && !data.isP || (this.state === 'BACKGROUND' && data.isP && targets[i*3+2] < -100)) {
                // Partículas flotantes en el fondo reciben un ruido senoidal suave
                positions[i*3+1] += Math.sin(time + data.noiseOffset) * 0.2;
                positions[i*3] += Math.cos(time + data.noiseOffset) * 0.1;
            } else if (Math.abs(targets[i*3] - positions[i*3]) < 1) {
                // Pequeña respiración cuando ya están en posición
                positions[i*3+1] += Math.sin(time * 2 + data.noiseOffset) * 0.05;
            }
        }

        this.geometry.attributes.position.needsUpdate = true;
        
        // Rotación general muy sutil para todo el sistema
        this.points.rotation.y = Math.sin(time * 0.5) * 0.05;
        this.points.rotation.x = Math.cos(time * 0.3) * 0.02;

        this.renderer.render(this.scene, this.camera);
    }
}

// Exportación para uso
// window.onload = () => {
//     new ProgrammableMatter('hero-canvas-container');
// };
