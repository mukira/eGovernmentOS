export class TimeSlider {
    constructor(containerId, onChange) {
        this.container = document.getElementById(containerId);
        this.onChange = onChange;
        this.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    }

    render() {
        this.container.innerHTML = `
      <div class="timeline-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px; color: var(--text-secondary);">
          <span>Past 6 Months</span>
          <span id="current-month-label">Today</span>
        </div>
        <input type="range" min="0" max="5" value="5" id="time-slider">
      </div>
    `;

        const slider = this.container.querySelector('#time-slider');
        slider.addEventListener('input', (e) => {
            const idx = parseInt(e.target.value);
            // Mock logic: 5 is "Today", 0 is "6 months ago"
            this.onChange(idx);
        });
    }
}
