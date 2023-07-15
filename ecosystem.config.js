module.exports = {
    apps: [
      {
        name: 'GrowTech_rest',
        script: 'manage.py',
        args: 'runserver',
        interpreter: 'python3',
        watch: true,
        autorestart: true,
      },
    ],
  };
  