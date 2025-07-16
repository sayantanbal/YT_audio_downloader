module.exports = {
  apps: [
    {
      name: 'youtube-downloader-backend',
      script: 'gunicorn',
      args: '--config gunicorn.conf.py wsgi:app',
      cwd: './backend',
      interpreter: 'none',
      env: {
        FLASK_ENV: 'production',
        FLASK_DEBUG: 'False'
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      error_file: './logs/backend-error.log',
      out_file: './logs/backend-out.log',
      log_file: './logs/backend-combined.log'
    },
    {
      name: 'youtube-downloader-frontend',
      script: 'serve',
      args: '-s dist -l 3000',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      error_file: './logs/frontend-error.log',
      out_file: './logs/frontend-out.log',
      log_file: './logs/frontend-combined.log'
    }
  ]
};
