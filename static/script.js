document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text-input');
    const currentCharCount = document.getElementById('current-chars');
    const generateBtn = document.getElementById('generate-btn');
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('results-container');
    const toggleCloning = document.getElementById('toggle-cloning');
    const cloningContent = document.getElementById('cloning-content');
    const promptSpeech = document.getElementById('prompt-speech');
    const fileLabel = document.getElementById('file-label');
    const langBtns = document.querySelectorAll('.lang-btn');

    // i18n setup
    const translations = {
        kk: {
            subtitle: "Қазақ тіліндегі мәтінді жоғары сапалы дыбысқа айналдыру құралы",
            input_label: "Мәтінді енгізіңіз:",
            input_placeholder: "Осы жерге қазақша мәтінді енгізіңіз...",
            script_type: "Жазу түрі (Script Type)",
            script_cyrillic: "Кририллица (Cyrillic)",
            script_arabic: "Төте жазу (Arabic)",
            inference_mode: "Инференция режимі (Inference Mode)",
            mode_direct: "Тікелей",
            mode_segmented: "Сегменттелген",
            voice_cloning: "🎙️ Дауысты клондау (Voice Cloning)",
            upload_label: "Аудио файлды таңдаңыз немесе осында сүйреңіз",
            prompt_text_label: "Аудио транскрипциясы (міндетті емес):",
            prompt_text_placeholder: "Аудио файлдағы мәтінді енгізіңіз...",
            generate_btn: "Генерациялау",
            loader_text: "Дыбыс дайындалуда...",
            alert_empty: "Мәтінді енгізіңіз!",
            result_header: "Дыбыс нәтижесі",
            download: "💾 Жүктеп алу (Download)",
            file_selected: "Таңдалды"
        },
        zh: {
            subtitle: "高品质哈萨克语语音合成工具",
            input_label: "请输入文本：",
            input_placeholder: "在此输入哈萨克语文本...",
            script_type: "书写体系 (Script Type)",
            script_cyrillic: "西里尔文 (Cyrillic)",
            script_arabic: "老文字 (Arabic)",
            inference_mode: "推理模式 (Inference Mode)",
            mode_direct: "直接模式",
            mode_segmented: "分段模式",
            voice_cloning: "🎙️ 声音克隆 (Voice Cloning)",
            upload_label: "选择音频文件或将其拖至此处",
            prompt_text_label: "音频转录文本（可选）：",
            prompt_text_placeholder: "输入音频文件中的文本...",
            generate_btn: "开始生成",
            loader_text: "正在合成语音...",
            alert_empty: "请输入文本！",
            result_header: "生成结果",
            download: "💾 下载音频 (Download)",
            file_selected: "已选择"
        }
    };

    let currentLang = localStorage.getItem('spark_lang') || 'kk';

    function setLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('spark_lang', lang);

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[lang][key]) {
                if (el.tagName === 'SPAN' && el.parentElement.tagName === 'BUTTON') {
                    // Keep icon if exists
                    const icon = el.textContent.match(/^[\d\w\s]*[^\w\s\d]/);
                    el.textContent = translations[lang][key];
                } else {
                    el.textContent = translations[lang][key];
                }
            }
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (translations[lang][key]) {
                el.placeholder = translations[lang][key];
            }
        });

        langBtns.forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
        });

        document.documentElement.lang = lang;
    }

    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            setLanguage(btn.getAttribute('data-lang'));
        });
    });

    // Initialize UI language
    setLanguage(currentLang);

    // Character counter
    textInput.addEventListener('input', () => {
        const length = textInput.value.length;
        currentCharCount.textContent = length;
        if (length > 2000) {
            currentCharCount.style.color = '#ef4444';
        } else {
            currentCharCount.style.color = '#94a3b8';
        }
    });

    // Accordion toggle
    toggleCloning.addEventListener('click', () => {
        cloningContent.classList.toggle('active');
        const arrow = toggleCloning.querySelector('.arrow');
        arrow.textContent = cloningContent.classList.contains('active') ? '▲' : '▼';
    });

    // File selection feedback
    promptSpeech.addEventListener('change', (e) => {
        const fileName = e.target.files[0]?.name;
        if (fileName) {
            fileLabel.querySelector('span').textContent = `${translations[currentLang].file_selected}: ${fileName}`;
            fileLabel.style.borderColor = 'var(--primary)';
        }
    });

    // Generate process
    generateBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) {
            alert(translations[currentLang].alert_empty);
            return;
        }

        const mode = document.querySelector('input[name="mode"]:checked').value;
        const script = document.querySelector('input[name="script"]:checked').value;
        const promptText = document.getElementById('prompt-text').value;

        const formData = new FormData();
        formData.append('text', text);
        formData.append('mode', mode);
        formData.append('script', script);
        formData.append('prompt_text', promptText);

        if (promptSpeech.files[0]) {
            formData.append('prompt_speech', promptSpeech.files[0]);
        }

        // Show loader
        loader.classList.remove('hidden');
        generateBtn.disabled = true;

        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error during generation');
            }

            const data = await response.json();
            if (data.success === false) {
                throw new Error(data.detail || 'Error during generation');
            }
            addAudioResult(data);
        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        } finally {
            loader.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });

    function addAudioResult(data) {
        const url = data.audio_url;
        const originalText = data.original_text; // Assuming backend returns original_text
        const convertedText = data.converted_text; // Assuming backend returns converted_text

        const resultCard = document.createElement('div');
        resultCard.className = 'result-card animate-in';

        // Use converted text if backend provided it, otherwise use original
        // Fix: Added fallbacks stage-by-stage to prevent "undefined" length error
        const display_text = convertedText || originalText || "Audio Result";
        const previewText = (display_text && display_text.length > 100)
            ? display_text.substring(0, 100) + '...'
            : (display_text || "");

        resultCard.innerHTML = `
            <div class="result-header">
                <h3 data-i18n="result_header">${translations[currentLang].result_header}</h3>
                <span class="result-time">${new Date().toLocaleTimeString()}</span>
            </div>
            <p class="result-text" style="font-size: 0.9rem; color: var(--text-dim); margin-bottom: 12px; font-style: italic;">
                "${previewText}"
            </p>
            <audio controls src="${url}"></audio>
            <div class="audio-actions">
                <a href="${url}" download class="download-link">${translations[currentLang].download}</a>
            </div>
        `;

        resultsContainer.prepend(resultCard);
        resultCard.scrollIntoView({ behavior: 'smooth' });
    }
});
