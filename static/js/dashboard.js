import Chart from 'https://cdn.jsdelivr.net/npm/chart.js';

let activityChart;

function updateStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('messagesCount').textContent = data.messages_processed;
            document.getElementById('usersCount').textContent = data.active_users;
            document.getElementById('errorsCount').textContent = data.errors;

            updateServicesStatus(data.services_status);
            updateChart(data);
        })
        .catch(error => console.error('Error fetching stats:', error));
}

function updateServicesStatus(status) {
    const servicesContainer = document.getElementById('servicesStatus');
    const services = {
        telegram: { name: 'Bot Telegram', icon: '🤖' },
        openai: { name: 'OpenAI', icon: '🧠' },
        twilio: { name: 'Twilio SMS', icon: '📱' },
        sendgrid: { name: 'SendGrid Email', icon: '📧' },
        firebase: { name: 'Firebase Auth', icon: '🔐' }
    };

    servicesContainer.innerHTML = Object.entries(status).map(([key, active]) => `
        <div class="service-status ${active ? 'active' : 'inactive'}">
            <div>
                <span class="me-2">${services[key].icon}</span>
                ${services[key].name}
            </div>
            <span class="badge ${active ? 'bg-success' : 'bg-danger'}">
                ${active ? 'Actif' : 'Non Configuré'}
            </span>
        </div>
    `).join('');
}

function updateChart(data) {
    if (!activityChart) {
        const ctx = document.getElementById('activityChart').getContext('2d');
        activityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Messages Traités',
                    data: [],
                    borderColor: 'rgb(0, 195, 255)',
                    backgroundColor: 'rgba(0, 195, 255, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: 'rgb(0, 195, 255)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(0, 195, 255)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#fff'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#fff'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animation: {
                    duration: 750,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    // Update chart data
    activityChart.data.labels.push(new Date().toLocaleTimeString());
    activityChart.data.datasets[0].data.push(data.messages_processed);

    // Keep only last 10 data points
    if (activityChart.data.labels.length > 10) {
        activityChart.data.labels.shift();
        activityChart.data.datasets[0].data.shift();
    }

    activityChart.update();
}

// Fonction pour charger les notifications
function loadNotifications() {
    fetch('/api/notifications')
        .then(response => response.json())
        .then(notifications => {
            const notificationsList = document.getElementById('notificationsList');
            const notificationCount = document.getElementById('notificationCount');

            notificationCount.textContent = notifications.length;
            notificationsList.innerHTML = notifications.map(n => `
                <div class="list-group-item bg-dark text-light border-secondary">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-1">${n.type === 'sms' ? '📱' : n.type === 'email' ? '📧' : '🤖'} ${n.message}</h6>
                        <small class="text-muted">${new Date(n.created_at).toLocaleString()}</small>
                    </div>
                </div>
            `).join('');
        });
}

// Fonction pour charger l'historique
function loadHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(history => {
            const historyTable = document.getElementById('messageHistory');
            historyTable.innerHTML = history.map(h => `
                <tr>
                    <td>${new Date(h.created_at).toLocaleString()}</td>
                    <td>${h.type === 'sms' ? '📱' : h.type === 'email' ? '📧' : '🤖'} ${h.type}</td>
                    <td>${h.content}</td>
                    <td><span class="badge ${h.status === 'sent' ? 'bg-success' : h.status === 'delivered' ? 'bg-info' : 'bg-danger'}">${h.status}</span></td>
                </tr>
            `).join('');
        });
}

// Mettre à jour toutes les 30 secondes
setInterval(() => {
    loadNotifications();
    loadHistory();
    updateStats();
}, 30000);

// Charger au démarrage
document.addEventListener('DOMContentLoaded', () => {
    loadNotifications();
    loadHistory();
    updateStats();
});

// Logout handler
document.getElementById('logoutBtn').addEventListener('click', () => {
    window.location.href = '/';
});