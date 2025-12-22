
import { GEEService } from './services/gee-service.js';
import { GEEAuthService } from './services/gee-auth.js';
import { HistoryService } from './services/history-service.js';
import { InsightCard } from './components/insight-card.js';

// Initialize Services
const authService = new GEEAuthService();
const geeService = new GEEService(authService);
const historyService = new HistoryService();

document.addEventListener('DOMContentLoaded', async () => {
    // DOM Elements
    const searchInput = document.getElementById('location-search');
    const sidePanel = document.getElementById('side-panel');
    const insightContent = document.getElementById('insight-content');
    const closeBtn = document.querySelector('.close-btn');

    // UI State Management
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            sidePanel.classList.remove('active');
        });
    }

    // 3. Filter Chips (Layer Toggling)
    // 3. Filter Chips (Layer Toggling) & Legend Control
    const chips = document.querySelectorAll('.chip-btn');
    const iframe = document.getElementById('map-frame') || document.getElementById('sandbox-frame');

    // Legend Elements
    const legend = document.getElementById('map-legend');
    const legendTitle = document.getElementById('legend-title');
    const legendSource = document.getElementById('legend-source');
    const legendGradient = document.getElementById('legend-gradient');
    const legendMin = document.getElementById('legend-min');
    const legendMax = document.getElementById('legend-max');

    const updateLegend = (layerId) => {
        if (!legend || !layerId) {
            if (legend) legend.classList.add('hidden');
            return;
        }

        // Dynamic Date (matches sandbox logic)
        const today = new Date();
        let lag = 1;
        if (layerId === 'FLOOD') lag = 2; // Matches map orbital gap logic
        if (layerId.includes('SMAP')) lag = 10;
        today.setDate(today.getDate() - lag);
        const dateStr = today.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

        // DISABLED: We are using the internal legend inside sandbox.html now
        legend.classList.add('hidden');
        return;

        /* 
        legend.classList.remove('hidden');
        if (legendSource) {
            // Show Loading Spinner initially
            legendSource.innerHTML = `<span class="legend-loader"></span> NASA Data • ${dateStr}`;
        }
        */

        switch (layerId) {
            case 'VEGETATION':
                legendTitle.textContent = 'Vegetation Health';
                legendMin.textContent = 'Stressed';
                legendMax.textContent = 'Healthy';
                // Brown/White to Deep Green
                legendGradient.style.background = 'linear-gradient(to right, #f5f5f5, #e5f5e0, #a1d99b, #31a354, #006d2c)';
                break;
            case 'FLOOD':
                legendTitle.textContent = 'Flood Risk Model';
                legendMin.textContent = 'Low Risk';
                legendMax.textContent = 'High Risk';
                // Light Blue to Dark Indigo (Vector colors)
                legendGradient.style.background = 'linear-gradient(to right, #9FA8DA, #5C6BC0, #283593)';
                break;
            case 'HEAT':
                legendTitle.textContent = 'Land Surface Temp';
                legendMin.textContent = '20°C';
                legendMax.textContent = '50°C+';
                // Yellow to Red
                legendGradient.style.background = 'linear-gradient(to right, #ffffb2, #fecc5c, #fd8d3c, #f03b20, #bd0026)';
                break;
            case 'AIR':
                legendTitle.textContent = 'Air Quality (AOD)';
                legendMin.textContent = 'Good';
                legendMax.textContent = 'Poor'; // AOD: Low is good, High is bad
                // White to Grey/Brown
                legendGradient.style.background = 'linear-gradient(to right, #ffffff, #d9d9d9, #969696, #525252)';
                break;
            case 'WATER':
                legendTitle.textContent = 'Atmospheric Water';
                legendMin.textContent = 'Dry';
                legendMax.textContent = 'Humid';
                // White to Blue
                legendGradient.style.background = 'linear-gradient(to right, #f7fbff, #deebf7, #9ecae1, #3182bd, #08519c)';
                break;
        }
    };

    // Listen for Map Idle (Loaded)
    window.addEventListener('message', (event) => {
        if (event.data.type === 'MAP_IDLE') {
            const loader = document.querySelector('.legend-loader');
            if (loader) {
                loader.remove(); // Remove spinner when tiles are ready
            }
        }
    });

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const isActive = chip.classList.contains('active');

            // Toggle UI (Radio behavior)
            chips.forEach(c => c.classList.remove('active'));

            let layerId = null;

            if (!isActive) {
                chip.classList.add('active');

                // Determine ID
                const text = chip.textContent.trim();
                if (text.includes('Vegetation')) layerId = 'VEGETATION';
                if (text.includes('Flood')) layerId = 'FLOOD';
                if (text.includes('Air')) layerId = 'AIR';
                if (text.includes('Heat')) layerId = 'HEAT';
                if (text.includes('Water')) layerId = 'WATER';
            }

            // Update Map
            iframe.contentWindow.postMessage({ type: 'SET_LAYER', layerId }, '*');

            // Update Legend
            updateLegend(layerId);
        });
    });

    // 1. Core Search Logic
    async function handleSearch() {
        const query = searchInput.value;
        if (!query) return;

        // Visual Feedback
        const searchBox = document.querySelector('.search-box');
        searchBox.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';

        try {
            await updateView(query);
        } catch (error) {
            console.error(error);
        }
    }

    // 2. Event Listeners
    searchInput.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') await handleSearch();
    });

    // Initialize Autocomplete
    const initAutocomplete = () => {
        if (!window.google || !window.google.maps || !window.google.maps.places) return;

        const autocomplete = new google.maps.places.Autocomplete(searchInput, {
            componentRestrictions: { country: 'ke' },
            fields: ['name']
        });

        autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            if (place && place.name) {
                searchInput.value = place.name;
                handleSearch();
            }
        });
    };

    // Try initializing immediately (if verified loaded)
    if (window.google && window.google.maps && window.google.maps.places) {
        initAutocomplete();
    } else {
        // Wait for async callback
        document.addEventListener('google-maps-loaded', initAutocomplete);
    }

    // Feature: Search Suggestions (Dual State: "This Area" Card vs. Major Towns List)

    // Data: Major Towns (Fallback if no history)
    const suggestionsData = [
        { type: 'history', title: 'Nairobi', subtitle: 'Kenya' },
        { type: 'history', title: 'Mombasa', subtitle: 'Mombasa County, Kenya' },
        { type: 'history', title: 'Kisumu', subtitle: 'Kisumu County, Kenya' },
        { type: 'history', title: 'Nakuru', subtitle: 'Nakuru County, Kenya' }
    ];

    let suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'pac-container';
    suggestionsContainer.style.display = 'none';
    suggestionsContainer.style.position = 'absolute';
    suggestionsContainer.style.zIndex = '1000';
    suggestionsContainer.style.left = '10px';
    suggestionsContainer.style.width = '392px';
    // Base styles
    suggestionsContainer.style.background = 'transparent';
    suggestionsContainer.style.boxShadow = 'none';
    suggestionsContainer.style.border = 'none';

    document.body.appendChild(suggestionsContainer);

    // Render "This Area" Card (Zero State)
    const renderZeroStateCard = () => {
        suggestionsContainer.innerHTML = '';
        suggestionsContainer.style.top = '65px'; // Detached

        // Add zero-state class for CSS override (Transparent BG / No Shadow)
        suggestionsContainer.classList.add('zero-state');

        // Clear conflicting inline styles to let CSS take over
        suggestionsContainer.style.background = '';
        suggestionsContainer.style.boxShadow = '';
        suggestionsContainer.style.borderRadius = '';
        suggestionsContainer.style.borderTop = '';

        const card = document.createElement('div');
        card.className = 'area-card';

        // Header
        const header = document.createElement('div');
        header.className = 'area-header';
        header.innerHTML = `
            <div class="area-title">This area</div>
            <div class="area-weather">
                <span style="margin-right: 8px;">23°</span>
                <span class="material-symbols-outlined" style="color: #70757a;">rainy</span>
            </div>
        `;

        // Content
        const content = document.createElement('div');
        content.className = 'area-content';
        content.innerHTML = `
            <div class="area-icon-circle">
                <span class="material-symbols-outlined" style="color: white; font-size: 20px;">flood</span>
            </div>
            <div class="area-info">
                <div class="area-headline">Heavy rainfall in this area</div>
                <div class="area-subtext">Typical conditions with risk of flooding</div>
            </div>
            <span class="material-symbols-outlined area-chevron">chevron_right</span>
        `;

        card.appendChild(header);
        card.appendChild(content);

        card.addEventListener('click', () => {
            searchInput.value = 'Nairobi';
            suggestionsContainer.style.display = 'none';
            handleSearch();
        });

        suggestionsContainer.appendChild(card);
        suggestionsContainer.style.display = 'block';
    };

    // Render Recent History / Towns List (Active State)
    const renderHistoryList = () => {
        suggestionsContainer.innerHTML = '';
        suggestionsContainer.style.top = '58px'; // Attached to search bar

        // Remove zero-state overrides
        suggestionsContainer.classList.remove('zero-state');

        // Style container to look like a list dropdown
        suggestionsContainer.style.background = 'white';
        suggestionsContainer.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.08)';
        suggestionsContainer.style.borderRadius = '0 0 24px 24px'; // Match search bar roundness
        suggestionsContainer.style.borderTop = '1px solid #e8eaed';

        suggestionsData.forEach(item => {
            const div = document.createElement('div');
            div.className = 'pac-item rich-item';

            const iconWrapper = document.createElement('div');
            iconWrapper.className = 'pac-icon-wrapper';

            const icon = document.createElement('span');
            icon.className = 'pac-icon-inside';
            icon.textContent = 'schedule'; // History clock

            iconWrapper.appendChild(icon);

            const content = document.createElement('div');
            content.className = 'pac-item-content';

            const title = document.createElement('div');
            title.className = 'pac-item-title';
            title.textContent = item.title;

            content.appendChild(title);

            if (item.subtitle) {
                const subtitle = document.createElement('div');
                subtitle.className = 'pac-item-subtitle';
                subtitle.textContent = item.subtitle;
                content.appendChild(subtitle);
            }

            div.appendChild(iconWrapper);
            div.appendChild(content);

            div.addEventListener('click', () => {
                searchInput.value = item.title;
                suggestionsContainer.style.display = 'none';
                handleSearch();
            });

            suggestionsContainer.appendChild(div);
        });

        // Add Footer
        const footer = document.createElement('div');
        footer.className = 'pac-footer';
        const footerLink = document.createElement('a');
        footerLink.className = 'pac-footer-link';
        footerLink.textContent = 'More from recent history';
        footer.appendChild(footerLink);
        suggestionsContainer.appendChild(footer);

        suggestionsContainer.style.display = 'block';
    };

    // 1. Initial Load: Show 'This Area' Card
    renderZeroStateCard();

    // 2. Interaction Logic
    // Click on Input -> Switch to History/Towns List
    searchInput.addEventListener('click', () => {
        if (!searchInput.value.trim()) {
            renderHistoryList();
        }
    });

    // Input Focus -> Same (Switch to List)
    searchInput.addEventListener('focus', () => {
        if (!searchInput.value.trim()) {
            renderHistoryList();
        }
    });

    // Input Typing -> Hide Custom, Let Google Autocomplete Take Over
    searchInput.addEventListener('input', () => {
        if (searchInput.value.trim()) {
            suggestionsContainer.style.display = 'none';
        } else {
            // Cleared input -> Show List again
            renderHistoryList();
        }
    });

    // Blur -> Revert to "This Area" card after delay
    searchInput.addEventListener('blur', () => {
        setTimeout(() => {
            // Always revert to Zero State card on blur
            renderZeroStateCard();
        }, 200);
    });

    const searchIcon = document.querySelector('.search-icon');
    if (searchIcon) {
        searchIcon.style.cursor = 'pointer';
        searchIcon.addEventListener('click', handleSearch);
    }

    const directionsBtn = document.querySelector('.search-btn');
    if (directionsBtn && !directionsBtn.classList.contains('date-picker-btn')) {
        directionsBtn.addEventListener('click', handleSearch);
    }

    // 6. Date Picker Logic
    const dateBtn = document.getElementById('date-picker-btn');
    const dateInput = document.getElementById('date-input');
    const dateDisplay = document.getElementById('date-display');

    if (dateBtn && dateInput) {
        // Initialize with Today
        const today = new Date();
        dateInput.valueAsDate = today;

        dateBtn.addEventListener('click', () => {
            // Modern API or fallback
            if (dateInput.showPicker) {
                dateInput.showPicker();
            } else {
                dateInput.click();
            }
        });

        dateInput.addEventListener('change', (e) => {
            const selected = new Date(e.target.value);
            const options = { year: 'numeric', month: 'short', day: 'numeric' };
            dateDisplay.textContent = selected.toLocaleDateString('en-US', options);

            // Future: Message sandbox to update Lag Days based on date diff
            // const diffDays = Math.ceil((today - selected) / (1000 * 60 * 60 * 24));
            // iframe.contentWindow.postMessage({ type: 'SET_DATE', lagDays: diffDays }, '*');
        });
    }

    // 5. Main View Update Logic
    async function updateView(region) {
        // Always show "This Area" card (Zero State) alongside results
        renderZeroStateCard();

        // UI: Show active state + Skeleton Loader
        sidePanel.classList.add('active');
        insightContent.innerHTML = `
            <div style="padding: 24px;">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text" style="width: 90%;"></div>
                <br>
                <div class="skeleton skeleton-rect"></div>
                <br>
                <div class="skeleton skeleton-title" style="width: 40%;"></div>
                <div class="skeleton skeleton-text"></div>
            </div>
        `;

        // Map: Pan to Region
        const mapFrame = document.getElementById('map-frame');
        if (mapFrame && mapFrame.contentWindow) {
            mapFrame.contentWindow.postMessage({ type: 'PAN_TO', region: region }, '*');
        }

        try {
            // Data: Fetch from Gemini/GEE
            const data = await geeService.getData(region);

            // Render: Insight Card
            const card = new InsightCard(data);
            insightContent.innerHTML = card.render();

            // History: Save Brief
            historyService.saveBrief(region, data.explanation, {
                ndvi: data.vegetationHealth.score / 100,
                flood_risk: data.floodRisk.level
            });

            // Actions: PDF & WhatsApp
            document.getElementById('btn-pdf')?.addEventListener('click', () => {
                window.print();
            });

            document.getElementById('btn-whatsapp')?.addEventListener('click', () => {
                const text = encodeURIComponent(`🚨 *FORECAST ALERT: ${data.region}*\n\n*Status*: ${data.explanation}\n*Action*: ${data.recommendation}`);
                const url = `https://wa.me/?text=${text}`;
                window.open(url, '_blank');
            });

        } catch (err) {
            console.error(err);
            insightContent.innerHTML = '<div style="color:#d93025; padding:24px; text-align:center;">Error loading data.</div>';
        }
    }
});
