db.auth('root', '12345')

db = db.getSiblingDB('kinoprogramm')

db.createUser({
  user: 'root',
  pwd: '12345',
  roles: [
    {
      role: 'readWrite',
      db: 'kinoprogramm',
    },
  ],
});