<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>未來科技 | Future Tech</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-color: #00f0ff;
            --secondary-color: #7b2ff7;
            --accent-color: #ff006e;
            --dark-bg: #0a0e27;
            --card-bg: rgba(255, 255, 255, 0.05);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--dark-bg);
            color: #fff;
            overflow-x: hidden;
            cursor: none;
        }

        /* 自定義游標 */
        .cursor {
            width: 20px;
            height: 20px;
            border: 2px solid var(--primary-color);
            border-radius: 50%;
            position: fixed;
            pointer-events: none;
            z-index: 9999;
            transition: 0.1s;
            transform: translate(-50%, -50%);
            box-shadow: 0 0 20px var(--primary-color);
        }

        .cursor-follower {
            width: 40px;
            height: 40px;
            border: 1px solid rgba(0, 240, 255, 0.3);
            border-radius: 50%;
            position: fixed;
            pointer-events: none;
            z-index: 9998;
            transition: 0.3s;
            transform: translate(-50%, -50%);
        }

        /* 背景動畫粒子 */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            background: var(--primary-color);
            border-radius: 50%;
            animation: float linear infinite;
            opacity: 0.6;
        }

        @keyframes float {
            0% {
                transform: translateY(100vh) scale(0);
                opacity: 0;
            }
            50% {
                opacity: 0.8;
            }
            100% {
                transform: translateY(-100vh) scale(1);
                opacity: 0;
            }
        }

        /* 導航欄 */
        nav {
            position: fixed;
            top: 0;
            width: 100%;
            padding: 20px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            background: rgba(10, 14, 39, 0.8);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 240, 255, 0.1);
        }

        .logo {
            font-size: 28px;
            font-weight: bold;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 240, 255, 0.5);
        }

        .nav-links {
            display: flex;
            gap: 40px;
            list-style: none;
        }

        .nav-links a {
            color: #fff;
            text-decoration: none;
            font-size: 16px;
            position: relative;
            transition: 0.3s;
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--primary-color);
            transition: 0.3s;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        .nav-links a:hover {
            color: var(--primary-color);
        }

        /* 主要內容區 */
        .hero {
            position: relative;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 1;
        }

        .hero-content {
            max-width: 900px;
            padding: 0 20px;
        }

        .hero h1 {
            font-size: 80px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #fff, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% {
                filter: drop-shadow(0 0 20px rgba(0, 240, 255, 0.5));
            }
            50% {
                filter: drop-shadow(0 0 40px rgba(0, 240, 255, 0.8));
            }
        }

        .hero p {
            font-size: 24px;
            margin-bottom: 40px;
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.6;
        }

        .cta-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 15px 40px;
            font-size: 18px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: 0.3s;
            position: relative;
            overflow: hidden;
            text-decoration: none;
            display: inline-block;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: #fff;
            box-shadow: 0 10px 30px rgba(0, 240, 255, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 240, 255, 0.5);
        }

        .btn-secondary {
            background: transparent;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
        }

        .btn-secondary:hover {
            background: var(--primary-color);
            color: var(--dark-bg);
            transform: translateY(-3px);
        }

        /* 特色區域 */
        .features {
            position: relative;
            padding: 100px 50px;
            z-index: 1;
        }

        .section-title {
            text-align: center;
            font-size: 48px;
            margin-bottom: 60px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .feature-card {
            background: var(--card-bg);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid rgba(0, 240, 255, 0.2);
            backdrop-filter: blur(10px);
            transition: 0.3s;
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(0, 240, 255, 0.1), transparent);
            transform: rotate(45deg);
            transition: 0.5s;
        }

        .feature-card:hover::before {
            left: 100%;
        }

        .feature-card:hover {
            transform: translateY(-10px);
            border-color: var(--primary-color);
            box-shadow: 0 20px 50px rgba(0, 240, 255, 0.3);
        }

        .feature-icon {
            font-size: 50px;
            margin-bottom: 20px;
            display: inline-block;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-10px);
            }
        }

        .feature-card h3 {
            font-size: 24px;
            margin-bottom: 15px;
            color: var(--primary-color);
        }

        .feature-card p {
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.6;
        }

        /* 統計數據區 */
        .stats {
            position: relative;
            padding: 80px 50px;
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(123, 47, 247, 0.1));
            z-index: 1;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }

        .stat-item {
            padding: 30px;
        }

        .stat-number {
            font-size: 60px;
            font-weight: bold;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .stat-label {
            font-size: 18px;
            color: rgba(255, 255, 255, 0.7);
        }

        /* 3D 卡片展示區 */
        .showcase {
            position: relative;
            padding: 100px 50px;
            z-index: 1;
        }

        .showcase-container {
            max-width: 1200px;
            margin: 0 auto;
            perspective: 1000px;
        }

        .card-3d {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 60px;
            border: 1px solid rgba(0, 240, 255, 0.2);
            backdrop-filter: blur(10px);
            transition: transform 0.5s;
            transform-style: preserve-3d;
        }

        .card-3d:hover {
            transform: rotateY(5deg) rotateX(5deg);
        }

        .showcase-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }

        .showcase-text h2 {
            font-size: 42px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .showcase-text p {
            font-size: 18px;
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.8;
            margin-bottom: 30px;
        }

        .showcase-image {
            position: relative;
            height: 400px;
            border-radius: 15px;
            overflow: hidden;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 100px;
        }

        /* 頁腳 */
        footer {
            position: relative;
            padding: 60px 50px 30px;
            background: rgba(0, 0, 0, 0.5);
            border-top: 1px solid rgba(0, 240, 255, 0.2);
            z-index: 1;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
            margin-bottom: 40px;
        }

        .footer-section h3 {
            color: var(--primary-color);
            margin-bottom: 20px;
            font-size: 20px;
        }

        .footer-section p,
        .footer-section a {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            line-height: 2;
            display: block;
        }

        .footer-section a:hover {
            color: var(--primary-color);
        }

        .social-links {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }

        .social-icon {
            width: 40px;
            height: 40px;
            background: var(--card-bg);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            font-size: 20px;
        }

        .social-icon:hover {
            background: var(--primary-color);
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 240, 255, 0.3);
        }

        .copyright {
            text-align: center;
            padding-top: 30px;
            border-top: 1px solid rgba(0, 240, 255, 0.1);
            color: rgba(255, 255, 255, 0.5);
        }

        /* 滾動動畫 */
        .fade-in {
            opacity: 0;
            transform: translateY(50px);
            transition: opacity 0.8s, transform 0.8s;
        }

        .fade-in.active {
            opacity: 1;
            transform: translateY(0);
        }

        /* 響應式設計 */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 48px;
            }

            .hero p {
                font-size: 18px;
            }

            .nav-links {
                display: none;
            }

            .showcase-content {
                grid-template-columns: 1fr;
            }

            .section-title {
                font-size: 36px;
            }
        }

        /* 載入動畫 */
        .loader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--dark-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            transition: opacity 0.5s, visibility 0.5s;
        }

        .loader.hidden {
            opacity: 0;
            visibility: hidden;
        }

        .loader-circle {
            width: 80px;
            height: 80px;
            border: 4px solid rgba(0, 240, 255, 0.2);
            border-top-color: var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
    </style>
</head>
<body>
    <!-- 載入動畫 -->
    <div class="loader">
        <div class="loader-circle"></div>
    </div>

    <!-- 自定義游標 -->
    <div class="cursor"></div>
    <div class="cursor-follower"></div>

    <!-- 背景粒子 -->
    <div class="particles" id="particles"></div>

    <!-- 導航欄 -->
    <nav>
        <div class="logo">⚡ FUTURE TECH</div>
        <ul class="nav-links">
            <li><a href="#home">首頁</a></li>
            <li><a href="#features">特色</a></li>
            <li><a href="#showcase">展示</a></li>
            <li><a href="#contact">聯絡</a></li>
        </ul>
    </nav>

    <!-- 主要區域 -->
    <section class="hero" id="home">
        <div class="hero-content">
            <h1>未來科技</h1>
            <p>探索無限可能，打造智能未來<br>讓科技改變生活，讓創新引領時代</p>
            <div class="cta-buttons">
                <a href="#" class="btn btn-primary">開始探索</a>
                <a href="#" class="btn btn-secondary">了解更多</a>
            </div>
        </div>
    </section>

    <!-- 統計數據 -->
    <section class="stats">
        <div class="stats-grid">
            <div class="stat-item fade-in">
                <div class="stat-number" data-target="1000">0</div>
                <div class="stat-label">活躍用戶</div>
            </div>
            <div class="stat-item fade-in">
                <div class="stat-number" data-target="500">0</div>
                <div class="stat-label">合作夥伴</div>
            </div>
            <div class="stat-item fade-in">
                <div class="stat-number" data-target="50">0</div>
                <div class="stat-label">國家地區</div>
            </div>
            <div class="stat-item fade-in">
                <div class="stat-number" data-target="99">0</div>
                <div class="stat-label">滿意度 %</div>
            </div>
        </div>
    </section>

    <!-- 特色區域 -->
    <section class="features" id="features">
        <h2 class="section-title">核心特色</h2>
        <div class="features-grid">
            <div class="feature-card fade-in">
                <div class="feature-icon">🚀</div>
                <h3>極速性能</h3>
                <p>採用最新技術架構，提供閃電般的響應速度，讓您的體驗流暢無比。</p>
            </div>
            <div class="feature-card fade-in">
                <div class="feature-icon">🔒</div>
                <h3>安全可靠</h3>
                <p>企業級安全防護，多重加密技術，保護您的數據安全無憂。</p>
            </div>
            <div class="feature-card fade-in">
                <div class="feature-icon">🎨</div>
                <h3>精美設計</h3>
                <p>現代化的UI設計，直觀的用戶界面，帶來賞心悅目的視覺體驗。</p>
            </div>
            <div class="feature-card fade-in">
                <div class="feature-icon">🌐</div>
                <h3>全球服務</h3>
                <p>覆蓋全球50+國家，24/7全天候服務，隨時隨地為您服務。</p>
            </div>
            <div class="feature-card fade-in">
                <div class="feature-icon">⚡</div>
                <h3>智能AI</h3>
                <p>整合先進AI技術，智能分析與預測，為您提供個性化解決方案。</p>
            </div>
            <div class="feature-card fade-in">
                <div class="feature-icon">📱</div>
                <h3>跨平台</h3>
                <p>完美支援各種設備，無論手機、平板還是電腦，都能完美運行。</p>
            </div>
        </div>
    </section>

    <!-- 展示區域 -->
    <section class="showcase" id="showcase">
        <div class="showcase-container">
            <div class="card-3d fade-in">
                <div class="showcase-content">
                    <div class="showcase-text">
                        <h2>創新技術解決方案</h2>
                        <p>我們致力於提供最前沿的技術解決方案，幫助企業實現數位轉型，提升競爭力。</p>
                        <p>透過AI、大數據、雲端運算等先進技術，為您打造專屬的智能生態系統。</p>
                        <a href="#" class="btn btn-primary">查看案例</a>
                    </div>
                    <div class="showcase-image">
                        💎
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 頁腳 -->
    <footer id="contact">
        <div class="footer-content">
            <div class="footer-section">
                <h3>關於我們</h3>
                <p>Future Tech 致力於推動科技創新，為全球用戶提供最優質的技術服務與解決方案。</p>
                <div class="social-links">
                    <a href="#" class="social-icon">📘</a>
                    <a href="#" class="social-icon">🐦</a>
                    <a href="#" class="social-icon">📷</a>
                    <a href="#" class="social-icon">💼</a>
                </div>
            </div>
            <div class="footer-section">
                <h3>快速連結</h3>
                <a href="#">產品服務</a>
                <a href="#">解決方案</a>
                <a href="#">客戶案例</a>
                <a href="#">技術支援</a>
            </div>
            <div class="footer-section">
                <h3>資源中心</h3>
                <a href="#">技術文檔</a>
                <a href="#">開發者API</a>
                <a href="#">部落格</a>
                <a href="#">常見問題</a>
            </div>
            <div class="footer-section">
                <h3>聯絡我們</h3>
                <p>📧 info@futuretech.com</p>
                <p>📞 +886 2 1234 5678</p>
                <p>📍 台北市信義區科技大道 100 號</p>
            </div>
        </div>
        <div class="copyright">
            <p>&copy; 2024 Future Tech. All rights reserved. | 隱私政策 | 服務條款</p>
        </div>
    </footer>

    <script>
        // 載入動畫
        window.addEventListener('load', () => {
            setTimeout(() => {
                document.querySelector('.loader').classList.add('hidden');
            }, 1000);
        });

        // 自定義游標
        const cursor = document.querySelector('.cursor');
        const cursorFollower = document.querySelector('.cursor-follower');

        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            
            setTimeout(() => {
                cursorFollower.style.left = e.clientX + 'px';
                cursorFollower.style.top = e.clientY + 'px';
            }, 100);
        });

        // 點擊效果
        document.addEventListener('mousedown', () => {
            cursor.style.transform = 'translate(-50%, -50%) scale(0.8)';
            cursorFollower.style.transform = 'translate(-50%, -50%) scale(1.5)';
        });

        document.addEventListener('mouseup', () => {
            cursor.style.transform = 'translate(-50%, -50%) scale(1)';
            cursorFollower.style.transform = 'translate(-50%, -50%) scale(1)';
        });

        // 生成背景粒子
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.width = Math.random() * 3 + 1 + 'px';
            particle.style.height = particle.style.width;
            particle.style.animationDuration = Math.random() * 10 + 10 + 's';
            particle.style.animationDelay = Math.random() * 5 + 's';
            particlesContainer.appendChild(particle);
        }

        // 滾動動畫
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });

        // 數字計數動畫
        const animateCounter = (element) => {
            const target = parseInt(element.getAttribute('data-target'));
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    element.textContent = Math.floor(current) + '+';
                    requestAnimationFrame(updateCounter);
                } else {
                    element.textContent = target + '+';
                }
            };

            updateCounter();
        };

        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const number = entry.target.querySelector('.stat-number');
                    if (number && !number.classList.contains('animated')) {
                        number.classList.add('animated');
                        animateCounter(number);
                    }
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.stat-item').forEach(item => {
            statsObserver.observe(item);
        });

        // 3D 卡片效果
        const card3d = document.querySelector('.card-3d');
        if (card3d) {
            card3d.addEventListener('mousemove', (e) => {
                const rect = card3d.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;
                
                card3d.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });

            card3d.addEventListener('mouseleave', () => {
                card3d.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            });
        }

        // 平滑滾動
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // 導航欄滾動效果
        let lastScroll = 0;
        const nav = document.querySelector('nav');

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > lastScroll && currentScroll > 100) {
                nav.style.transform = 'translateY(-100%)';
            } else {
                nav.style.transform = 'translateY(0)';
            }
            
            lastScroll = currentScroll;
        });

        // 按鈕波紋效果
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.5)';
                ripple.style.transform = 'scale(0)';
                ripple.style.animation = 'ripple 0.6s ease-out';
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });

        // 添加波紋動畫
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
