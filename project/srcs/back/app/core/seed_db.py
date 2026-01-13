import random
from faker import Faker
from datetime import datetime, timedelta

import bcrypt


fake = Faker()

def get_seed_data(db, count=500):
    TEST_PASSWORD_HASH =bcrypt.hashpw(
            "password".encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
    
    genders = ['male', 'female', 'other']
    prefs = ['straight', 'gay', 'bisexual']
    tags_pool = ['coding', 'fitness', 'art', 'music', 'travel', 'gaming', 'sushi', 'hiking', 'photography', 'yoga', 'reading', 'cooking', 'dancing', 'movies', 'pets']

    try:
        with db.get_cursor(commit=True) as cur:

            cur.executemany("INSERT INTO tags (name) VALUES (%s) ON CONFLICT DO NOTHING", [(t,) for t in tags_pool])
            cur.execute("SELECT id FROM tags")
            tag_ids = [r[0] for r in cur.fetchall()]

            user_ids = []
            for i in range(count):
                username = f"test_user_{i}" if i < 10 else fake.unique.user_name()
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = f"test{i}@example.com" if i < 10 else fake.unique.email()

                cur.execute("""
                    INSERT INTO users (username, first_name, last_name, password_hash, email, fame_rating, latitude, longitude, is_verified)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, True) RETURNING id
                """, (username, first_name, last_name, 
                      TEST_PASSWORD_HASH, email, 0.0,
                      float(fake.latitude()), float(fake.longitude())))
                user_ids.append(cur.fetchone()[0])

            for u_id in user_ids:
                cur.execute("INSERT INTO profiles (user_id, gender, sexual_preference, biography) VALUES (%s, %s, %s, %s)",
                    (u_id, random.choice(genders), random.choice(prefs), fake.paragraph(nb_sentences=3)))
                
                chosen_tags = random.sample(tag_ids, random.randint(2, 5))
                cur.executemany("INSERT INTO user_interests (user_id, tag_id) VALUES (%s, %s)", [(u_id, t_id) for t_id in chosen_tags])

                num_pictures = random.randint(3, 5)
                picture_urls = [f"https://picsum.photos/seed/{fake.uuid4()}/600/600" for _ in range(num_pictures)]   
                profile_pic_url = random.choice(picture_urls)

                for url in picture_urls:
                    is_profile = (url == profile_pic_url)
                    cur.execute("""
                        INSERT INTO user_pictures (user_id, url, is_profile_picture)
                        VALUES (%s, %s, %s)
                    """, (u_id, url, is_profile))

            for i in range(len(user_ids) // 2):
                u1, u2 = random.sample(user_ids, 2)
                
                cur.execute("INSERT INTO user_interactions (liker_id, liked_id, status) VALUES (%s, %s, 'liked') ON CONFLICT DO NOTHING", (u1, u2))
                cur.execute("INSERT INTO user_interactions (liker_id, liked_id, status) VALUES (%s, %s, 'liked') ON CONFLICT DO NOTHING", (u2, u1))

                cur.execute("""
                    INSERT INTO conversations (user1_id, user2_id) VALUES (%s, %s) 
                    ON CONFLICT DO NOTHING RETURNING id
                """, (u1, u2))
                
                conv_id_result = cur.fetchone()
                if conv_id_result:
                    conv_id = conv_id_result[0]

                    messages_data = [
                        (u1, "salut", datetime.now() - timedelta(minutes=random.randint(50, 60))),
                        (u2, "salut", datetime.now() - timedelta(minutes=random.randint(40, 50))),
                        (u1, "cv?", datetime.now() - timedelta(minutes=random.randint(30, 40))),
                        (u2, "cv hmd et toi?", datetime.now() - timedelta(minutes=random.randint(20, 30))),
                        (u1, "cv hmd", datetime.now() - timedelta(minutes=random.randint(10, 20))),
                        (u2, "ewa?", datetime.now() - timedelta(minutes=random.randint(1, 10)))
                    ]
                    
                    for sender_id, text, sent_time in messages_data:
                        cur.execute("""
                            INSERT INTO messages (conversation_id, sender_id, content, sent_at, is_read)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (conv_id, sender_id, text, sent_time, random.choice([True, False])))

    except Exception as e:
        print(f"ERROR Gen dummy users: {e}", flush=True)
        raise