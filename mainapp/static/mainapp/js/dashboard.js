const SENSOR_MAP = {
    temperature: { valueEl: document.getElementById('temperature-value'), timeEl: document.getElementById('temperature-time') },
    humidity: { valueEl: document.getElementById('humidity-value'), timeEl: document.getElementById('humidity-time') },
    light: { valueEl: document.getElementById('light-value'), timeEl: document.getElementById('light-time') },
};

let chart;
let currentPage = 1;
let totalPages = 1;

async function fetchLatest() {
    try {
        const response = await fetch('/api/latest/');
        const data = await response.json();
        Object.entries(data.latest).forEach(([key, reading]) => {
            const sensor = SENSOR_MAP[key];
            if (!sensor) return;
            if (reading.value !== null) {
                sensor.valueEl.textContent = `${reading.value.toFixed(1)}`;
                sensor.timeEl.textContent = `更新時間：${reading.timestamp}`;
            } else {
                sensor.valueEl.textContent = '--';
                sensor.timeEl.textContent = '資料尚未接收';
            }
        });
    } catch (error) {
        console.error('fetchLatest error:', error);
    }
}

async function fetchHistory() {
    try {
        const response = await fetch('/api/history/?days=7');
        const data = await response.json();
        const labels = data.timestamps;
        const temperatureData = data.history.temperature || [];
        const humidityData = data.history.humidity || [];
        const lightData = data.history.light || [];

        const ctx = document.getElementById('history-chart').getContext('2d');
        if (chart) {
            chart.data.labels = labels;
            chart.data.datasets[0].data = temperatureData;
            chart.data.datasets[1].data = humidityData;
            chart.data.datasets[2].data = lightData;
            chart.update();
            return;
        }

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: '溫度',
                        data: temperatureData,
                        borderColor: '#6cc7ff',
                        backgroundColor: 'rgba(108, 199, 255, 0.18)',
                        tension: 0.3,
                        pointRadius: 2,
                    },
                    {
                        label: '濕度',
                        data: humidityData,
                        borderColor: '#7ef59d',
                        backgroundColor: 'rgba(126, 245, 157, 0.18)',
                        tension: 0.3,
                        pointRadius: 2,
                    },
                    {
                        label: '光照度',
                        data: lightData,
                        borderColor: '#e89cff',
                        backgroundColor: 'rgba(232, 156, 255, 0.18)',
                        tension: 0.3,
                        pointRadius: 2,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { color: '#aac8ff' },
                        grid: { color: 'rgba(255,255,255,0.08)' },
                    },
                    y: {
                        ticks: { color: '#aac8ff' },
                        grid: { color: 'rgba(255,255,255,0.08)' },
                    },
                },
                plugins: {
                    legend: { labels: { color: '#e8efff' } },
                },
            },
        });
    } catch (error) {
        console.error('fetchHistory error:', error);
    }
}

async function fetchRecords(page = 1) {
    const type = document.getElementById('filter-type').value;
    const dateFrom = document.getElementById('date-from').value;
    const dateTo = document.getElementById('date-to').value;
    const query = new URLSearchParams({ page, type, date_from: dateFrom, date_to: dateTo });

    try {
        const response = await fetch(`/api/records/?${query.toString()}`);
        const data = await response.json();
        const tbody = document.getElementById('records-body');
        tbody.innerHTML = '';

        data.records.forEach((record) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${record.sensor_type}</td>
                <td>${record.value}</td>
                <td>${record.timestamp}</td>
            `;
            tbody.appendChild(row);
        });

        currentPage = data.page;
        totalPages = data.num_pages;
        document.getElementById('page-info').textContent = `${currentPage} / ${totalPages}`;
    } catch (error) {
        console.error('fetchRecords error:', error);
    }
}

function setupListeners() {
    document.getElementById('load-records').addEventListener('click', () => fetchRecords(1));
    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) fetchRecords(currentPage - 1);
    });
    document.getElementById('next-page').addEventListener('click', () => {
        if (currentPage < totalPages) fetchRecords(currentPage + 1);
    });
}

async function init() {
    await fetchLatest();
    await fetchHistory();
    await fetchRecords();
    setupListeners();
    setInterval(fetchLatest, 3000);
}

init();
