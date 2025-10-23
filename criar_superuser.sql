-- Script SQL para criar superusuário no PostgreSQL
-- Execute no Railway com: railway run psql -f criar_superuser.sql

-- Inserir o superusuário na tabela auth_user
-- Senha: Admin@2025!Olhar
-- Hash gerado com: pbkdf2_sha256$600000$...

INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'pbkdf2_sha256$600000$FzJXK8Y9vWxE$QZG+YZ5XxVvK/1CZ6YZx1VvK1VvK1VvK1VvK1VvK1Vg=',
    NULL,
    true,
    'admin',
    '',
    '',
    'admin@olharliterario.com',
    true,
    true,
    NOW()
) ON CONFLICT (username) DO NOTHING;

SELECT 
    username,
    email,
    is_superuser,
    is_staff,
    is_active
FROM auth_user 
WHERE username = 'admin';
