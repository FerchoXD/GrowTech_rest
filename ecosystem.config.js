module.exports = {
    apps: [
      {
        name: 'GrowTech_rest',
        script: 'manage.py',
        args: 'runserver',
        interpreter: 'python',
        watch: true,
        autorestart: true,
      },
    ],
  };
  