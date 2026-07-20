document.addEventListener('DOMContentLoaded', () => {
    // State management
    const state = {
        apiKey: localStorage.getItem('cenciel_openai_key') || '',
        activePage: 'overview',
        marketResult: null,
        vocResult: null,
        selectedSellingPoint: '',
        contentResult: null,
        instagramActiveSlide: 0
    };

    // DOM Elements Cache
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.app-page');
    const statusTextEl = document.getElementById('status-text');
    const settingsApiKeyInput = document.getElementById('settings-api-key');
    const saveSettingsBtn = document.getElementById('save-settings');

    // Page Switching Logic
    function switchPage(pageId) {
        state.activePage = pageId;

        // Update sidebar links
        document.querySelectorAll('.nav-item').forEach(item => {
            if (item.dataset.page === pageId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Update content pages view
        pages.forEach(page => {
            if (page.id === `page-${pageId}`) {
                page.classList.add('active');
            } else {
                page.classList.remove('active');
            }
        });

        // Track active node in visualizer
        document.querySelectorAll('.pipeline-node').forEach(node => {
            if (node.dataset.step === pageId) {
                node.classList.add('active');
            } else {
                node.classList.remove('active');
            }
        });
    }

    // Nav Bindings
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const pageId = e.currentTarget.closest('.nav-item').dataset.page;
            switchPage(pageId);
        });
    });

    // Overview Pipeline Flow Clicks
    document.querySelectorAll('.diagram-step').forEach(step => {
        step.addEventListener('click', (e) => {
            const pageId = e.currentTarget.dataset.target;
            switchPage(pageId);
        });
    });

    // Update global status to Cenciel AI Active
    function updateStatusIndicator() {
        if (statusTextEl) {
            statusTextEl.textContent = 'Cenciel AI Active';
        }
        const dot = document.querySelector('.status-dot');
        if (dot) {
            dot.style.background = '#10b981';
            dot.style.boxShadow = '0 0 10px #10b981';
        }
    }

    updateStatusIndicator();

    // ==========================================
    // STEP 1: MARKET RADAR
    // ==========================================
    const marketForm = document.getElementById('market-form');
    const marketInput = document.getElementById('market-input');
    const marketLoading = document.getElementById('market-loading');
    const marketResultsSection = document.getElementById('market-results-section');
    const marketKeywordsContainer = document.getElementById('market-keywords');
    const marketUspContainer = document.getElementById('market-usp-list');
    const marketTargetingContainer = document.getElementById('market-targeting-list');
    const proceedToVocBtn = document.getElementById('proceed-to-voc-btn');

    if (marketForm) {
        marketForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const inputVal = marketInput.value.trim();
            if (!inputVal) return;

            // UI loading transition
            marketResultsSection.style.display = 'none';
            marketLoading.style.display = 'flex';

            // Set dynamic loading text
            const loadingTexts = [
                "경쟁사 데이터를 스크랩핑하고 있습니다...",
                "소셜 버즈 데이터와 쇼핑 리뷰를 파싱 중입니다...",
                "LLM 마케팅 기획 모델이 트렌드를 추적하고 있습니다..."
            ];
            let textIdx = 0;
            const textInterval = setInterval(() => {
                textIdx = (textIdx + 1) % loadingTexts.length;
                document.getElementById('market-loading-text').textContent = loadingTexts[textIdx];
            }, 1000);

            try {
                const response = await fetch('/api/analyze-market', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': state.apiKey
                    },
                    body: JSON.stringify({ input: inputVal })
                });

                if (response.ok) {
                    const data = await response.json();
                    state.marketResult = data;
                    renderMarketResults(data);
                } else {
                    alert('시장분석을 진행하는 중 오류가 발생했습니다.');
                }
            } catch (err) {
                console.error(err);
                alert('네트워크 연결에 문제가 발생했습니다.');
            } finally {
                clearInterval(textInterval);
                marketLoading.style.display = 'none';
            }
        });
    }

    function renderMarketResults(data) {
        // Render search keywords
        marketKeywordsContainer.innerHTML = '';
        data.llm_data.keywords.forEach(kw => {
            const span = document.createElement('span');
            span.className = 'tag-badge';
            span.textContent = kw;
            marketKeywordsContainer.appendChild(span);
        });

        // Render competitor USP cards
        marketUspContainer.innerHTML = '';
        data.llm_data.usp.forEach(item => {
            const card = document.createElement('div');
            card.className = 'usp-card';
            card.innerHTML = `
                <div class="usp-card-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" /></svg>
                    <span>${item.title}</span>
                </div>
                <div class="usp-card-desc">${item.desc}</div>
            `;
            marketUspContainer.appendChild(card);
        });

        // Render targeting directions
        marketTargetingContainer.innerHTML = '';
        data.llm_data.targeting.forEach(item => {
            const div = document.createElement('div');
            div.className = 'strategy-item';
            div.innerHTML = `
                <div class="strategy-target">🎯 ${item.target}</div>
                <div class="strategy-approach">${item.strategy}</div>
            `;
            marketTargetingContainer.appendChild(div);
        });

        // Make section visible
        marketResultsSection.style.display = 'block';
        marketResultsSection.scrollIntoView({ behavior: 'smooth' });

        // Bind Proceed button
        if (proceedToVocBtn) {
            proceedToVocBtn.onclick = () => {
                // If it was a cosmetic keyword, pre-populate VOC reviews textarea with sample cosmetic feedback
                const vocTextarea = document.getElementById('voc-text-input');
                if (vocTextarea) {
                    if (data.crawler_data.title.includes("PDRN") || marketInput.value.includes("PDRN")) {
                        vocTextarea.value = "신제품 PDRN 끈적이지 않는다고 했는데, 역시 고농축이라 아침에 화장 전 바르면 다 밀려요.. 제형 개선 시급\nPDRN 성분 함량이 높아서 그런지 확실히 피부 장벽 개박살 난 곳 재생은 잘 되는 기분입니다. 근데 향이 약간 좀 피시한? 향이 나요.\n일주일 썼는데 건조하진 않음. 미끈거리는 감이 오래 유지되어서 지성 쓰기엔 무거울 거 같네요.\n사용하고 트러블 안 남! 스포이트 용기가 묵직해서 잘 안 빨아당겨지는데 그게 아쉬움.\n끈적끈적하지만 밤에 바르고 자면 다음 날 아침 꿀피부 됨. 화장 전엔 절대 금지\n피부 장벽 개선되는 거 하난 탑티어인 듯. 근데 입구 부분에 제형이 굳어서 위생상 지저분해 보임.";
                    } else {
                        vocTextarea.value = "속건조 정말 심한 수부지인데 저녁에 바르고 자도 아침엔 살짝 당기네요. 보습력이 아침까지 안 가는 듯.\n흡수 하나는 엄청 빨라요. 화장 밀림도 전혀 없고 쏙 들어가서 아침 스킨케어로 좋음.\n바른 후에 살짝 쓰라린 자극이 있네요. 성분이 강한가 싶어요.\n속피부에 수분이 공급되는 느낌. 근데 저녁에는 이 위에 보습 크림 한 겹 더 얹어야 속당김이 완벽히 해결됨!!\n민감하고 여드름성 피부인데 이거 바른 뒤로 볼에 좁쌀처럼 살짝 붉게 트러블 올라와요ㅠㅠ 안심 성분 맞나요?\n300Da 초저분자라고 해서 기대했는데 보습 유지 수분 쉴드는 좀 얇은 거 같아요.";
                    }
                }
                switchPage('voc');
            };
        }
    }

    // ==========================================
    // STEP 2: VOC & REVIEWS ANALYSIS
    // ==========================================
    const vocPasteForm = document.getElementById('voc-paste-form');
    const vocTextInput = document.getElementById('voc-text-input');
    const vocFileZone = document.getElementById('voc-file-zone');
    const vocFileInput = document.getElementById('file-input');
    const vocLoading = document.getElementById('voc-loading');
    const vocResultsSection = document.getElementById('voc-results-section');
    const vocAnalyzePastedBtn = document.getElementById('voc-analyze-pasted-btn');

    // Upload event triggers
    if (vocFileZone && vocFileInput) {
        vocFileZone.addEventListener('click', () => vocFileInput.click());

        vocFileZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            vocFileZone.classList.add('dragover');
        });

        vocFileZone.addEventListener('dragleave', () => {
            vocFileZone.classList.remove('dragover');
        });

        vocFileZone.addEventListener('drop', (e) => {
            e.preventDefault();
            vocFileZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                vocFileInput.files = e.dataTransfer.files;
                handleVOCFileUpload(e.dataTransfer.files[0]);
            }
        });

        vocFileInput.addEventListener('change', () => {
            if (vocFileInput.files.length) {
                handleVOCFileUpload(vocFileInput.files[0]);
            }
        });
    }

    async function handleVOCFileUpload(file) {
        vocResultsSection.style.display = 'none';
        vocLoading.style.display = 'flex';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload-voc', {
                method: 'POST',
                headers: {
                    'X-API-Key': state.apiKey
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                state.vocResult = data;
                renderVOCResults(data);
            } else {
                const errData = await response.json();
                alert(`파일 분석 중 오류 발생: ${errData.detail || '알 수 없는 오류'}`);
            }
        } catch (err) {
            console.error(err);
            alert('파일 전송 실패: 네트워크 상태를 확인해 주세요.');
        } finally {
            vocLoading.style.display = 'none';
        }
    }

    // Analyze pasted reviews
    if (vocAnalyzePastedBtn) {
        vocAnalyzePastedBtn.addEventListener('click', async () => {
            const rawText = vocTextInput.value.trim();
            if (!rawText) {
                alert('리뷰 텍스트를 입력해 주세요!');
                return;
            }

            vocResultsSection.style.display = 'none';
            vocLoading.style.display = 'flex';

            try {
                const response = await fetch('/api/analyze-voc', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': state.apiKey
                    },
                    body: JSON.stringify({ text: rawText })
                });

                if (response.ok) {
                    const data = await response.json();
                    state.vocResult = data;
                    renderVOCResults(data);
                } else {
                    alert('VOC 파싱 중 오류가 발생했습니다.');
                }
            } catch (err) {
                console.error(err);
                alert('분석 실패: 네트워크 오류 발생.');
            } finally {
                vocLoading.style.display = 'none';
            }
        });
    }

    function renderVOCResults(data) {
        // Set volume statistics
        document.getElementById('voc-total-reviews').textContent = data.stats.valid_reviews_count;
        document.getElementById('voc-stat-col-name').innerHTML = data.stats.detected_text_column
            ? `감지된 텍스트 열: <strong>${data.stats.detected_text_column}</strong>`
            : `텍스트 분석 완료`;

        // Render mini rating distribution (horizontal progress bars)
        const ratContainer = document.getElementById('voc-ratings-chart-container');
        ratContainer.innerHTML = '';
        if (data.stats.has_ratings) {
            // Stars progress bars
            const dist = data.stats.rating_distribution;
            const maxVal = Math.max(...Object.values(dist)) || 1;

            Object.keys(dist).sort((a, b) => b - a).forEach(ratingKey => {
                const count = dist[ratingKey];
                const pct = Math.round((count / maxVal) * 100);

                const scoreRow = document.createElement('div');
                scoreRow.style.display = 'flex';
                scoreRow.style.alignItems = 'center';
                scoreRow.style.gap = '0.5rem';
                scoreRow.style.marginBottom = '0.4rem';
                scoreRow.style.fontSize = '0.8rem';

                scoreRow.innerHTML = `
                    <span style="width: 48px; color: var(--text-secondary); text-align: right;">${ratingKey} Star</span>
                    <div style="flex-grow: 1; height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow:hidden;">
                        <div style="width: ${pct}%; height:100%; background: var(--primary-grad); border-radius: 4px;"></div>
                    </div>
                    <span style="width: 25px; color: #fff; text-align: left; font-weight: 700;">${count}</span>
                `;
                ratContainer.appendChild(scoreRow);
            });
        } else {
            ratContainer.innerHTML = `
                <div style="text-align: center; color: var(--text-muted); font-size: 0.82rem; padding: 1rem 0;">
                    별점 정보가 존재하지 않아<br>텍스트 마이닝 통계만 노출되었습니다.
                </div>
            `;
        }

        // Render core pain points
        const painContainer = document.getElementById('voc-pain-list');
        painContainer.innerHTML = '';
        data.llm_data.pain_points.forEach(item => {
            const badgeClass = item.count >= 4 ? 'impact-high' : 'impact-med';
            const badgeLabel = item.count >= 4 ? 'High Impact' : 'Med Impact';
            const element = document.createElement('div');
            element.className = 'pain-item';
            element.innerHTML = `
                <div class="pain-meta">
                    <span class="pain-category">${item.category}</span>
                    <span class="pain-desc">${item.complaint}</span>
                </div>
                <span class="impact-badge ${badgeClass}">${badgeLabel}</span>
            `;
            painContainer.appendChild(element);
        });

        // Render Ideas Table
        const ideaTbody = document.querySelector('#voc-ideas-table tbody');
        ideaTbody.innerHTML = '';
        data.llm_data.ideas.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <div class="idea-concept">💡 ${item.concept}</div>
                </td>
                <td>${item.desc}</td>
            `;
            ideaTbody.appendChild(tr);
        });

        // Render derived Selling Points (핵심 소구점) with click mechanics
        const spContainer = document.getElementById('voc-sp-list');
        spContainer.innerHTML = '';
        data.llm_data.selling_points.forEach((sp, idx) => {
            const card = document.createElement('div');
            card.className = 'sp-item-card';
            card.dataset.spText = sp;
            card.innerHTML = `
                <div class="sp-radio"></div>
                <div class="sp-text">${sp}</div>
                <div class="sp-action-indicator">
                    <span>이동하기</span>
                    <svg style="width: 14px; height: 14px;" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                </div>
            `;

            card.addEventListener('click', () => {
                document.querySelectorAll('.sp-item-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                state.selectedSellingPoint = sp;

                // Prefill step 3 input
                const contentInput = document.getElementById('content-selling-point');
                if (contentInput) {
                    contentInput.value = sp;
                }

                // Dynamic flow jump to Step 3
                switchPage('generator');
            });
            spContainer.appendChild(card);
        });

        // Make section visible
        vocResultsSection.style.display = 'block';
        vocResultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // ==========================================
    // STEP 3: CONTENT GENERATOR
    // ==========================================
    const generatorForm = document.getElementById('generator-form');
    const contentSellingPointInput = document.getElementById('content-selling-point');
    const generatorLoading = document.getElementById('generator-loading');
    const generatorResultsSection = document.getElementById('generator-results-section');

    // Channel subtab switching
    const tabButtons = document.querySelectorAll('.channel-tab');
    const tabPanels = document.querySelectorAll('.channel-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const channel = btn.dataset.channel;

            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            tabPanels.forEach(p => {
                if (p.id === `channel-${channel}`) {
                    p.classList.add('active');
                } else {
                    p.classList.remove('active');
                }
            });
        });
    });

    if (generatorForm) {
        generatorForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const spVal = contentSellingPointInput.value.trim();
            if (!spVal) {
                alert('소구점 1줄을 입력하거나 2단계 VOC 분석 결과에서 선택해 주세요!');
                return;
            }

            generatorResultsSection.style.display = 'none';
            generatorLoading.style.display = 'flex';

            try {
                const response = await fetch('/api/generate-content', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': state.apiKey
                    },
                    body: JSON.stringify({ selling_point: spVal })
                });

                if (response.ok) {
                    const data = await response.json();
                    state.contentResult = data;
                    renderContentResults(data);
                } else {
                    alert('원고 생성 중 오류가 발생했습니다.');
                }
            } catch (err) {
                console.error(err);
                alert('콘텐츠 로드 중 예상치 못한 요류가 발견되었습니다.');
            } finally {
                generatorLoading.style.display = 'none';
            }
        });
    }

    function renderContentResults(data) {
        // Hide/Show outputs
        generatorResultsSection.style.display = 'block';
        generatorResultsSection.scrollIntoView({ behavior: 'smooth' });

        // 1. INSTAGRAM PANEL
        const instaData = data.llm_data.instagram;

        // Caption and hashtags
        const capEl = document.getElementById('insta-mock-caption-content');
        if (capEl) capEl.innerHTML = instaData.caption.replace(/\n/g, '<br>');

        const hashEl = document.getElementById('insta-mock-hashtags');
        if (hashEl) hashEl.textContent = instaData.hashtags.map(h => `#${h}`).join(' ');

        // Render card storyboard list
        const storyboardWrapper = document.getElementById('insta-storyboard');
        storyboardWrapper.innerHTML = '';

        instaData.slides.forEach((slide, idx) => {
            const slideItem = document.createElement('div');
            slideItem.className = `story-slide-item ${idx === 0 ? 'active' : ''}`;
            slideItem.innerHTML = `
                <div class="slide-num-badge">${slide.num}</div>
                <div class="slide-content-text">
                    <div class="slide-header-text">${slide.title}</div>
                    <div class="slide-desc-text">${slide.content}</div>
                </div>
            `;

            slideItem.addEventListener('click', () => {
                document.querySelectorAll('.story-slide-item').forEach(el => el.classList.remove('active'));
                slideItem.classList.add('active');
                state.instagramActiveSlide = idx;
                updatePhoneSlidePreview(instaData.slides[idx]);
            });

            storyboardWrapper.appendChild(slideItem);
        });

        // Initialize Phone visual slide
        updatePhoneSlidePreview(instaData.slides[0]);

        // 2. NAVER BLOG PANEL
        const blogData = data.llm_data.naver_blog;
        document.getElementById('blog-render-title').textContent = blogData.title;

        // Structure the body text
        const blogBodyWrapper = document.getElementById('blog-render-body');
        blogBodyWrapper.innerHTML = '';

        // Add intro
        const introP = document.createElement('p');
        introP.className = 'blog-para';
        introP.innerHTML = blogData.intro.replace(/\n/g, '<br>');
        blogBodyWrapper.appendChild(introP);

        // Add subheadings and paragraphs
        blogData.body.forEach(section => {
            const h3 = document.createElement('h3');
            h3.className = 'blog-h3';
            h3.innerHTML = `✏️ ${section.header}`;

            const p = document.createElement('p');
            p.className = 'blog-para';
            p.innerHTML = section.content.replace(/\n/g, '<br>');

            blogBodyWrapper.appendChild(h3);
            blogBodyWrapper.appendChild(p);
        });

        // Add outro
        const outroP = document.createElement('p');
        outroP.className = 'blog-para';
        outroP.style.fontWeight = '700'; // Make call to action standout
        outroP.innerHTML = blogData.outro.replace(/\n/g, '<br>');
        blogBodyWrapper.appendChild(outroP);

        // 3. SHORT FORM PANEL
        const sfData = data.llm_data.shortform;
        document.getElementById('sf-concept-text').textContent = sfData.concept;

        const sfTbody = document.querySelector('#sf-script-table tbody');
        sfTbody.innerHTML = '';
        sfData.scenes.forEach(scene => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="time-col">${scene.time}</td>
                <td class="visual-col">🎥 ${scene.visual}</td>
                <td class="audio-col">🎙️ ${scene.audio}</td>
            `;
            sfTbody.appendChild(tr);
        });

        // Initialize Copy-to-Clipboard Buttons
        bindClipboardCopy('copy-insta-caption-btn', instaData.caption + '\n\n' + instaData.hashtags.map(h => `#${h}`).join(' '));
        bindClipboardCopy('copy-blog-content-btn', getBlogCopyString(blogData));
        bindClipboardCopy('copy-sf-script-btn', getShortformCopyString(sfData));
    }

    function updatePhoneSlidePreview(slideData) {
        document.getElementById('phone-media-num').textContent = `Slide ${slideData.num}`;
        document.getElementById('phone-media-title').textContent = slideData.title;
        document.getElementById('phone-media-body').textContent = slideData.content;

        // Update slide dot indicator inside phone
        const dotsContainer = document.getElementById('phone-media-dots');
        dotsContainer.innerHTML = '';
        if (state.contentResult) {
            state.contentResult.llm_data.instagram.slides.forEach((_, idx) => {
                const dot = document.createElement('div');
                dot.className = `media-dot ${idx === state.instagramActiveSlide ? 'active' : ''}`;
                dotsContainer.appendChild(dot);
            });
        }
    }

    // Helper functions for clipboard formatting
    function bindClipboardCopy(btnId, textToCopy) {
        const btn = document.getElementById(btnId);
        if (!btn) return;

        btn.addEventListener('click', () => {
            navigator.clipboard.writeText(textToCopy).then(() => {
                const origHtml = btn.innerHTML;
                btn.innerHTML = `
                    <svg style="width:14px;height:14px;" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                    <span>복사 완료!</span>
                `;
                setTimeout(() => {
                    btn.innerHTML = origHtml;
                }, 2000);
            }).catch(err => {
                console.error(err);
                alert('복사 중 오류가 발생했습니다.');
            });
        });
    }

    function getBlogCopyString(blogData) {
        let content = `제목: ${blogData.title}\n\n`;
        content += `${blogData.intro}\n\n`;
        blogData.body.forEach(sec => {
            content += `${sec.header}\n${sec.content}\n\n`;
        });
        content += `${blogData.outro}`;
        return content;
    }

    function getShortformCopyString(sfData) {
        let content = `숏폼 컨셉: ${sfData.concept}\n\n`;
        sfData.scenes.forEach(sec => {
            content += `[시간: ${sec.time}]\n화면: ${sec.visual}\n오디오: ${sec.audio}\n\n`;
        });
        return content;
    }
});
