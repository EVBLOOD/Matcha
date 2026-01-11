-- Drop tables if exits / Just for now
DROP TABLE IF EXISTS "user_interests" CASCADE;
DROP TABLE IF EXISTS "user_pictures" CASCADE;
DROP TABLE IF EXISTS "user_interactions" CASCADE;
DROP TABLE IF EXISTS "profile_views" CASCADE;
DROP TABLE IF EXISTS "messages" CASCADE;
DROP TABLE IF EXISTS "conversations" CASCADE;
DROP TABLE IF EXISTS "notifications" CASCADE;
DROP TABLE IF EXISTS "user_blocks" CASCADE;
DROP TABLE IF EXISTS "user_reports" CASCADE;
DROP TABLE IF EXISTS "tags" CASCADE;
DROP TABLE IF EXISTS "profiles" CASCADE;
DROP TABLE IF EXISTS "users" CASCADE;

-- Create tables with the propreties I'll need

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    -- password_hash CHAR(60) NOT NULL,
    password_hash CHAR(60), -- if null means it's oauth
    email VARCHAR(255) UNIQUE NOT NULL,
    fame_rating INT DEFAULT 0 NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    verification_token VARCHAR(50) UNIQUE,
    is_verified BOOLEAN DEFAULT FALSE,
    last_online TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profiles (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    gender VARCHAR(20) CHECK (gender IN ('male', 'female', 'other')),
    sexual_preference VARCHAR(20) CHECK (sexual_preference IN ('straight', 'gay', 'bisexual')),
    biography TEXT,
    location_set_by_user BOOLEAN DEFAULT FALSE
);

CREATE TABLE user_pictures (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    url VARCHAR(255) NOT NULL,
    is_profile_picture BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user_interests (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, tag_id)
);

CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    liker_id INT REFERENCES users(id) ON DELETE CASCADE,
    liked_id INT REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(10) NOT NULL CHECK (status IN ('liked', 'disliked')),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (liker_id, liked_id)
);

CREATE TABLE profile_views (
    id SERIAL PRIMARY KEY,
    viewer_id INT REFERENCES users(id) ON DELETE CASCADE,
    viewed_id INT REFERENCES users(id) ON DELETE CASCADE,
    viewed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user1_id INT REFERENCES users(id) ON DELETE CASCADE,
    user2_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id INT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    sent_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);


CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('like', 'view', 'message', 'match', 'unmatch')),
    source_user_id INT REFERENCES users(id) ON DELETE SET NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_blocks (
    blocker_id INT REFERENCES users(id) ON DELETE CASCADE,
    blocked_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (blocker_id, blocked_id)
);

CREATE TABLE user_reports (
    id SERIAL PRIMARY KEY,
    reporter_id INT REFERENCES users(id) ON DELETE CASCADE,
    reported_id INT REFERENCES users(id) ON DELETE CASCADE,
    reason TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
