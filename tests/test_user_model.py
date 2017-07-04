from datetime import datetime

import time
import unittest

from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_password_setter(self):
    #     u = User(password='cat')
    #     self.assertTrue(u.password_hash is not None)

    # def test_no_password_getter(self):
    #     u = User(password='cat')
    #     with self.assertRaises(AttributeError):
    #         u.password

    # def test_password_verification(self):
    #     u = User(password='cat')
    #     self.assertTrue(u.verify_password('cat'))
    #     self.assertFalse(u.verify_password('dog'))

    # def test_password_salts_are_random(self):
    #     u = User(password='cat')
    #     u2 = User(password='cat')
    #     self.assertTrue(u.password_hash != u2.password_hash)

    # def test_valid_confirmation_token(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token()
    #     self.assertTrue(u.confirm(token))

    # def test_invalid_confirmation_token(self):
    #     u1 = User(password='cat')
    #     u2 = User(password='dog')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     token = u1.generate_confirmation_token()
    #     self.assertFalse(u2.confirm(token))

    # def test_expired_confirmation_token(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token(1)
    #     time.sleep(2)
    #     self.assertFalse(u.confirm(token))

    # def test_valid_reset_token(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_reset_token()
    #     self.assertTrue(u.reset_password(token, 'dog'))
    #     self.assertTrue(u.verify_password('dog'))

    # def test_invalid_reset_token(self):
    #     u1 = User(password='cat')
    #     u2 = User(password='dog')
    #     db.session.add_all([u1, u2])
    #     db.session.commit()
    #     token = u1.generate_reset_token()
    #     self.assertFalse(u2.reset_password(token, 'horse'))
    #     self.assertTrue(u2.verify_password('dog'))

    # def test_valid_email_change_token(self):
    #     u = User(email='ravil@example.com', password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_email_change_token('gal_ravil@example.com')
    #     self.assertTrue(u.change_email(token))
    #     self.assertTrue(u.email == 'gal_ravil@example.com')

    # def test_invalid_email_change_token(self):
    #     u1 = User(email='ravil@example.com', password='cat')
    #     u2 = User(email='user@example.com', password='dog')
    #     db.session.add_all([u1, u2])
    #     db.session.commit()
    #     token = u2.generate_email_change_token('ravil@example.com')
    #     self.assertFalse(u2.change_email(token))
    #     self.assertTrue(u2.email == 'user@example.com')

    # def test_roles_and_permissions(self):
    #     u = User(email='john@example.com', password='bad')
    #     self.assertTrue(u.can(Permission.WRITE_ARTICLES))
    #     self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    # def test_anonymous_user(self):
    #     u = AnonymousUser()
    #     self.assertFalse(u.can(Permission.FOLLOW))

    # def test_timestamps(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     self.assertTrue(
    #         (datetime.utcnow() - u.member_since).total_seconds() < 3
    #     )
    #     self.assertTrue(
    #         (datetime.utcnow() - u.last_seen).total_seconds() < 3
    #     )

    # def test_ping(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     time.sleep(2)
    #     last_seen_before = u.last_seen
    #     u.ping()
    #     self.assertTrue(u.last_seen > last_seen_before)

    # def test_gravatar(self):
    #     u = User(email='john@example.com', password='cat')
    #     with self.app.test_request_context('/'):
    #         gravatar_256 = u.gravatar(size=256)
    #         gravatar_pg = u.gravatar(rating='pg')
    #         gravatar_retro = u.gravatar(default='retro')
    #     self.assertTrue('s=256' in gravatar_256)
    #     self.assertTrue('r=pg' in gravatar_pg)
    #     self.assertTrue('d=retro' in gravatar_retro)

    def test_follow(self):
        u1 = User(email='john@example.com', password='111')
        u2 = User(email='susan@example.org', password='222')
        
        u1.follow(u2)

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_followed_by(u1))

        self.assertFalse(u2.is_following(u1))
        self.assertFalse(u1.is_followed_by(u2))

        self.assertTrue(u1.followed.count() == 1)
        self.assertTrue(u2.followers.count() == 1)
        self.assertTrue(Follow.query.count() == 1)

        f1 = u1.followed.all()[-1]
        self.assertTrue(f1.followed == u2)

        f2 = u2.followers.all()[-1]
        self.assertTrue(f2.follower == u1)


    def test_unfollow(self):
        u1 = User(email='john@example.com', password='111')
        u2 = User(email='susan@example.org', password='222')

        u1.follow(u2)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_followed_by(u1))
        
        u1.unfollow(u2)
        db.session.add(u1)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_followed_by(u1))

        self.assertTrue(u1.followed.count() == 0)
        self.assertTrue(u2.followers.count() == 0)
        self.assertTrue(Follow.query.count() == 0)


    def test_follow_timestamp(self):
        u1 = User(email='john@example.com', password='111')
        u2 = User(email='susan@example.org', password='222')

        timestamp_before = datetime.utcnow()

        u1.follow(u2)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        f = u1.followed.all()[-1]

        timestamp_after = datetime.utcnow()
        self.assertTrue(timestamp_before <= f.timestamp <= timestamp_after)