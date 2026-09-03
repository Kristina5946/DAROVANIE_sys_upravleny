-- phpMyAdmin SQL Dump
-- version 5.2.1-1.el8
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Июл 17 2026 г., 11:37
-- Версия сервера: 8.0.25-15
-- Версия PHP: 8.2.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `u3569663_localhost2`
--
CREATE DATABASE IF NOT EXISTS `u3569663_localhost2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `u3569663_localhost2`;

-- --------------------------------------------------------

--
-- Структура таблицы `accounts_userprofile`
--

CREATE TABLE `accounts_userprofile` (
  `id` bigint NOT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `accounts_userprofile`
--

INSERT INTO `accounts_userprofile` (`id`, `role`, `user_id`) VALUES
(1, 'director', 1),
(2, 'reception', 2),
(3, 'director', 3);

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Настройки центра', 9, 'add_centersettings'),
(26, 'Can change Настройки центра', 9, 'change_centersettings'),
(27, 'Can delete Настройки центра', 9, 'delete_centersettings'),
(28, 'Can view Настройки центра', 9, 'view_centersettings'),
(29, 'Can add Кабинет', 10, 'add_classroom'),
(30, 'Can change Кабинет', 10, 'change_classroom'),
(31, 'Can delete Кабинет', 10, 'delete_classroom'),
(32, 'Can view Кабинет', 10, 'view_classroom'),
(33, 'Can add Направление', 11, 'add_direction'),
(34, 'Can change Направление', 11, 'change_direction'),
(35, 'Can delete Направление', 11, 'delete_direction'),
(36, 'Can view Направление', 11, 'view_direction'),
(37, 'Can add Родитель', 15, 'add_parent'),
(38, 'Can change Родитель', 15, 'change_parent'),
(39, 'Can delete Родитель', 15, 'delete_parent'),
(40, 'Can view Родитель', 15, 'view_parent'),
(41, 'Can add Запись аудита', 8, 'add_auditlog'),
(42, 'Can change Запись аудита', 8, 'change_auditlog'),
(43, 'Can delete Запись аудита', 8, 'delete_auditlog'),
(44, 'Can view Запись аудита', 8, 'view_auditlog'),
(45, 'Can add Задача', 12, 'add_kanbantask'),
(46, 'Can change Задача', 12, 'change_kanbantask'),
(47, 'Can delete Задача', 12, 'delete_kanbantask'),
(48, 'Can view Задача', 12, 'view_kanbantask'),
(49, 'Can add Закупка материалов', 13, 'add_materialpurchase'),
(50, 'Can change Закупка материалов', 13, 'change_materialpurchase'),
(51, 'Can delete Закупка материалов', 13, 'delete_materialpurchase'),
(52, 'Can view Закупка материалов', 13, 'view_materialpurchase'),
(53, 'Can add Новость', 14, 'add_newsitem'),
(54, 'Can change Новость', 14, 'change_newsitem'),
(55, 'Can delete Новость', 14, 'delete_newsitem'),
(56, 'Can view Новость', 14, 'view_newsitem'),
(57, 'Can add Ученик', 20, 'add_student'),
(58, 'Can change Ученик', 20, 'change_student'),
(59, 'Can delete Ученик', 20, 'delete_student'),
(60, 'Can view Ученик', 20, 'view_student'),
(61, 'Can add Оплата', 16, 'add_payment'),
(62, 'Can change Оплата', 16, 'change_payment'),
(63, 'Can delete Оплата', 16, 'delete_payment'),
(64, 'Can view Оплата', 16, 'view_payment'),
(65, 'Can add Поднаправление', 21, 'add_subdirection'),
(66, 'Can change Поднаправление', 21, 'change_subdirection'),
(67, 'Can delete Поднаправление', 21, 'delete_subdirection'),
(68, 'Can view Поднаправление', 21, 'view_subdirection'),
(69, 'Can add Абонемент', 22, 'add_subscription'),
(70, 'Can change Абонемент', 22, 'change_subscription'),
(71, 'Can delete Абонемент', 22, 'delete_subscription'),
(72, 'Can view Абонемент', 22, 'view_subscription'),
(73, 'Can add Преподаватель', 23, 'add_teacher'),
(74, 'Can change Преподаватель', 23, 'change_teacher'),
(75, 'Can delete Преподаватель', 23, 'delete_teacher'),
(76, 'Can view Преподаватель', 23, 'view_teacher'),
(77, 'Can add Разовое занятие', 19, 'add_singlelesson'),
(78, 'Can change Разовое занятие', 19, 'change_singlelesson'),
(79, 'Can delete Разовое занятие', 19, 'delete_singlelesson'),
(80, 'Can view Разовое занятие', 19, 'view_singlelesson'),
(81, 'Can add Слот расписания', 18, 'add_scheduleslot'),
(82, 'Can change Слот расписания', 18, 'change_scheduleslot'),
(83, 'Can delete Слот расписания', 18, 'delete_scheduleslot'),
(84, 'Can view Слот расписания', 18, 'view_scheduleslot'),
(85, 'Can add Посещение', 7, 'add_attendancerecord'),
(86, 'Can change Посещение', 7, 'change_attendancerecord'),
(87, 'Can delete Посещение', 7, 'delete_attendancerecord'),
(88, 'Can view Посещение', 7, 'view_attendancerecord'),
(89, 'Can add Исключение в расписании', 17, 'add_scheduleexception'),
(90, 'Can change Исключение в расписании', 17, 'change_scheduleexception'),
(91, 'Can delete Исключение в расписании', 17, 'delete_scheduleexception'),
(92, 'Can view Исключение в расписании', 17, 'view_scheduleexception'),
(93, 'Can add Расчёт ЗП за период', 24, 'add_teacherpayrollperiod'),
(94, 'Can change Расчёт ЗП за период', 24, 'change_teacherpayrollperiod'),
(95, 'Can delete Расчёт ЗП за период', 24, 'delete_teacherpayrollperiod'),
(96, 'Can view Расчёт ЗП за период', 24, 'view_teacherpayrollperiod'),
(97, 'Can add Профиль сотрудника', 25, 'add_userprofile'),
(98, 'Can change Профиль сотрудника', 25, 'change_userprofile'),
(99, 'Can delete Профиль сотрудника', 25, 'delete_userprofile'),
(100, 'Can view Профиль сотрудника', 25, 'view_userprofile');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$KwVYMobU0XcTVSp2VD7hnK$eJlOvW0moR3PMQKv5Pl6AUo6R0mieMm9PaAULjIN/sQ=', '2026-07-17 07:55:39.082008', 1, 'admin', '', '', 'admin@darovanie.local', 1, 1, '2026-06-18 06:14:52.804988'),
(2, 'pbkdf2_sha256$1000000$c07m66bzuwnKWKAZXoroe4$9ooiLytC2UPbp7VkgQL3Da9eKqFlqVs34jp31xPGdGA=', '2026-07-17 08:05:24.125237', 0, 'Elena', '', '', '', 0, 1, '2026-07-01 14:48:28.868358'),
(3, 'pbkdf2_sha256$1000000$0XEMscoH66yByeH9ZZjpdH$nuo8GSoI5stALJC/AFGRZp1PeJPwN0tXRE257cz+weY=', '2026-07-07 21:33:34.926234', 0, 'Nataliya-director', '', '', '', 1, 1, '2026-07-07 21:27:55.687610');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_attendancerecord`
--

CREATE TABLE `core_attendancerecord` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lesson_date` date NOT NULL,
  `present` tinyint(1) NOT NULL,
  `paid` tinyint(1) NOT NULL,
  `note` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `schedule_slot_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `single_lesson_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `student_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `subscription_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_attendancerecord`
--

INSERT INTO `core_attendancerecord` (`created_at`, `updated_at`, `id`, `lesson_date`, `present`, `paid`, `note`, `direction_id`, `schedule_slot_id`, `single_lesson_id`, `student_id`, `subscription_id`) VALUES
('2026-07-07 22:58:09.149359', '2026-07-07 22:58:09.149402', '05308020450241bbaabdd4e955049a39', '2026-07-29', 0, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '31cddb9484894e66aa6beefd98a466cc', 'b71942feae48453e9a8b10b8b1bf0286'),
('2026-07-07 22:52:44.849626', '2026-07-17 07:56:42.479418', '0bc92e3dc6e345d593d530eb8607a213', '2026-07-13', 1, 1, 'Абонемент', '69c8b06ff95d4e8bb2e7db8f5117cfda', '6d972bc1300f45a49b5533ff5b451adb', NULL, '6400cbcc622f4ccc9417933f597a97f7', 'dd69f06eab9045bfbee354cb55e6b728'),
('2026-07-07 22:54:16.292840', '2026-07-17 07:57:11.337121', '11fd44276d704e47bf87eebc4d04feaa', '2026-07-15', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'e242d081296344ee8236925557a53439', '89e2f3ef904d4acbab83410a4ee7362e'),
('2026-07-07 22:36:51.353505', '2026-07-07 23:20:19.960197', '294ec0ffdc3147cb92e45abbaffb35f0', '2026-07-01', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '6400cbcc622f4ccc9417933f597a97f7', '009cac92d10e4dd19cdc46c0ceda60a8'),
('2026-07-07 23:00:01.515888', '2026-07-07 23:44:22.591580', '2cbdde3e15a34257b274295165bb3e69', '2026-07-07', 1, 1, 'Абонемент', '1f086e154be447cbacb8d682e5117527', '8274b9a656f74e53bd2aa32e1c86f43b', NULL, 'eac9ac0253564743b6a695fc1af487df', 'd28fb46e69a3494d8a7f1e973c6bb58c'),
('2026-07-07 23:00:16.146263', '2026-07-17 07:56:42.481804', '32a03b1eaa5e49779c641764382eb4f0', '2026-07-13', 1, 1, 'Абонемент', '69c8b06ff95d4e8bb2e7db8f5117cfda', '6d972bc1300f45a49b5533ff5b451adb', NULL, 'eac9ac0253564743b6a695fc1af487df', '96bef82f9fd44fa58c3d555a072ea570'),
('2026-07-07 21:38:35.890455', '2026-07-09 12:04:57.321129', '359d705554ae4aedb01591511888cac8', '2026-07-08', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '31cddb9484894e66aa6beefd98a466cc', 'b71942feae48453e9a8b10b8b1bf0286'),
('2026-07-17 08:05:47.047924', '2026-07-17 08:06:47.979722', '361a13d8a09a48938e38170d8d291a92', '2026-07-16', 1, 1, 'дополнительное', '4bcf75ed7c514f829af369a0b517a42f', NULL, '7b938857cbea46ed891db27996bace35', '31cddb9484894e66aa6beefd98a466cc', 'b71942feae48453e9a8b10b8b1bf0286'),
('2026-07-07 22:38:29.204427', '2026-07-07 23:20:05.625999', '48275d12e1bf409c8411b31b4d9ef3c9', '2026-07-06', 1, 1, 'Абонемент', '69c8b06ff95d4e8bb2e7db8f5117cfda', '6d972bc1300f45a49b5533ff5b451adb', NULL, '6400cbcc622f4ccc9417933f597a97f7', 'dd69f06eab9045bfbee354cb55e6b728'),
('2026-07-07 23:00:21.954162', '2026-07-17 07:57:11.337923', '5f74e7f8544c420794c82c7066d6643e', '2026-07-15', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'eac9ac0253564743b6a695fc1af487df', 'ce490832ce55405ca7332412545edcf2'),
('2026-07-07 21:38:35.900772', '2026-07-09 12:04:57.323151', '64639d2604194f0090a9d00073562de0', '2026-07-08', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'eac9ac0253564743b6a695fc1af487df', 'ce490832ce55405ca7332412545edcf2'),
('2026-07-17 08:04:38.478205', '2026-07-17 08:06:51.215036', '65a9e75e92cb4eeea09591b69134430f', '2026-07-16', 1, 1, 'дополнительное', '4bcf75ed7c514f829af369a0b517a42f', NULL, '1ad50f5a70eb4311ac5a406370572846', 'e242d081296344ee8236925557a53439', NULL),
('2026-07-07 22:38:20.167937', '2026-07-07 22:38:24.514726', '684f8ba793eb41f9ac8c6e28a7d63a11', '2026-07-04', 1, 1, '', 'e229ce3d79d648d9a86a4588ae3b83dd', NULL, 'd81f562bd50b4ca08cc41402f4ca544a', '31cddb9484894e66aa6beefd98a466cc', NULL),
('2026-07-17 08:01:45.685351', '2026-07-17 08:02:46.348959', '6a6f15987d0744e784ad7b4b200c92c9', '2026-07-14', 1, 1, 'дополнительное', '1f086e154be447cbacb8d682e5117527', NULL, 'f7bdfe1f6ffd436e8d7f4a407037612e', '31cddb9484894e66aa6beefd98a466cc', '529805dee6e245f4b9554f150566671d'),
('2026-07-07 22:36:51.370259', '2026-07-07 23:20:19.985915', '7104edb007694b6790b140aadb7f8e5d', '2026-07-01', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'e242d081296344ee8236925557a53439', '89e2f3ef904d4acbab83410a4ee7362e'),
('2026-07-07 23:01:03.328280', '2026-07-17 08:15:06.151642', '76dbf9207b934ab9be47fd229ff1b200', '2026-07-07', 1, 1, 'Абонемент', '9ebac65a5cc046f8a67274ee04397fec', '97542447921a4cc6bad0bdb5fc9ce9d4', NULL, 'eac9ac0253564743b6a695fc1af487df', '6e8fea899ac5484eb40f82fa96f1dd94'),
('2026-07-07 22:58:32.600780', '2026-07-07 23:20:45.863411', '7c9c4be437c04b5a87260900ed8b8dd1', '2026-07-07', 1, 1, 'Абонемент', '1f086e154be447cbacb8d682e5117527', '8274b9a656f74e53bd2aa32e1c86f43b', NULL, '31cddb9484894e66aa6beefd98a466cc', '529805dee6e245f4b9554f150566671d'),
('2026-07-07 22:56:43.771713', '2026-07-17 07:57:11.334940', '7db3da63e8654d02b04d83e5c1536c7e', '2026-07-15', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '6400cbcc622f4ccc9417933f597a97f7', '009cac92d10e4dd19cdc46c0ceda60a8'),
('2026-07-07 21:38:35.885045', '2026-07-09 12:04:57.313471', '7edc461defb341a18a06f53b73cba4fc', '2026-07-08', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '6400cbcc622f4ccc9417933f597a97f7', '009cac92d10e4dd19cdc46c0ceda60a8'),
('2026-07-17 08:06:31.088275', '2026-07-17 08:06:39.750795', '8cbb9244c8974223b5af8317aebac86d', '2026-07-16', 1, 1, 'дополнительное', '4bcf75ed7c514f829af369a0b517a42f', NULL, 'e4e917f5921d4250adb86ee14758005f', 'eac9ac0253564743b6a695fc1af487df', NULL),
('2026-07-07 22:54:16.312458', '2026-07-07 22:54:16.312504', '8dc283eaa5a047948d0832aabf178f67', '2026-07-29', 0, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'e242d081296344ee8236925557a53439', '89e2f3ef904d4acbab83410a4ee7362e'),
('2026-07-07 22:54:16.301715', '2026-07-07 22:54:16.301759', '8eef643e83084480a54ccde1126f9883', '2026-07-22', 0, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'e242d081296344ee8236925557a53439', '89e2f3ef904d4acbab83410a4ee7362e'),
('2026-07-07 22:36:51.376185', '2026-07-07 23:44:22.596338', '91d2be514d9940e4afe648e7919fc7ab', '2026-07-01', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'eac9ac0253564743b6a695fc1af487df', 'ce490832ce55405ca7332412545edcf2'),
('2026-07-09 12:04:36.546770', '2026-07-17 07:56:48.696793', '9945a21b1499430b82e619054e109b04', '2026-07-09', 1, 1, 'Абонемент', 'e229ce3d79d648d9a86a4588ae3b83dd', 'd249d49c51d84363acaf35f2e0e15bc5', NULL, '31cddb9484894e66aa6beefd98a466cc', 'dd99bf01cf634d92974b1aa3f095e02e'),
('2026-07-07 22:40:03.897388', '2026-07-17 07:56:42.480928', '9d8c92d86e9444af909ca541917300e5', '2026-07-13', 1, 1, 'Абонемент', '69c8b06ff95d4e8bb2e7db8f5117cfda', '6d972bc1300f45a49b5533ff5b451adb', NULL, 'e242d081296344ee8236925557a53439', '2ad3a703c37e471e8acd08389e14e623'),
('2026-07-07 23:01:03.337708', '2026-07-17 08:15:15.105334', '9f1f235aa33b4adcbf9530ce2e8ba05e', '2026-07-14', 0, 1, 'Абонемент', '9ebac65a5cc046f8a67274ee04397fec', '97542447921a4cc6bad0bdb5fc9ce9d4', NULL, 'eac9ac0253564743b6a695fc1af487df', '6e8fea899ac5484eb40f82fa96f1dd94'),
('2026-07-07 21:38:35.895638', '2026-07-09 12:04:57.322218', 'b2f2392f32064307b7bfee64b1c99681', '2026-07-08', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, 'e242d081296344ee8236925557a53439', '89e2f3ef904d4acbab83410a4ee7362e'),
('2026-07-07 23:27:50.135072', '2026-07-17 07:57:31.528281', 'b385561c71dc47b1be38dcec0500a01a', '2026-07-16', 0, 1, 'Абонемент', 'e229ce3d79d648d9a86a4588ae3b83dd', 'd249d49c51d84363acaf35f2e0e15bc5', NULL, '31cddb9484894e66aa6beefd98a466cc', 'dd99bf01cf634d92974b1aa3f095e02e'),
('2026-07-07 22:38:29.212507', '2026-07-07 23:44:22.594017', 'b5b4072b01864cbd8ada8ac7fe88c98e', '2026-07-06', 1, 1, 'Абонемент', '69c8b06ff95d4e8bb2e7db8f5117cfda', '6d972bc1300f45a49b5533ff5b451adb', NULL, 'eac9ac0253564743b6a695fc1af487df', '96bef82f9fd44fa58c3d555a072ea570'),
('2026-07-07 23:00:01.532511', '2026-07-17 07:56:33.850913', 'cbfd924925e243409525ec13d779ad19', '2026-07-14', 1, 1, 'Абонемент', '1f086e154be447cbacb8d682e5117527', '8274b9a656f74e53bd2aa32e1c86f43b', NULL, 'eac9ac0253564743b6a695fc1af487df', 'd28fb46e69a3494d8a7f1e973c6bb58c'),
('2026-07-17 08:02:30.379689', '2026-07-17 08:02:43.998975', 'cd173484bcd84ee98275e023db747854', '2026-07-14', 1, 1, 'дополнительное', '1f086e154be447cbacb8d682e5117527', NULL, '0fccbaf00910495cb051a965d5b25e6a', 'eac9ac0253564743b6a695fc1af487df', 'd28fb46e69a3494d8a7f1e973c6bb58c'),
('2026-07-07 22:58:32.608197', '2026-07-17 07:56:33.849884', 'd02136d26b4746889b549104fd4135a5', '2026-07-14', 1, 1, 'Абонемент', '1f086e154be447cbacb8d682e5117527', '8274b9a656f74e53bd2aa32e1c86f43b', NULL, '31cddb9484894e66aa6beefd98a466cc', '529805dee6e245f4b9554f150566671d'),
('2026-07-07 22:58:09.133637', '2026-07-17 07:57:11.336296', 'd8c1832caafe4427ae85620a181311ac', '2026-07-15', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '31cddb9484894e66aa6beefd98a466cc', 'b71942feae48453e9a8b10b8b1bf0286'),
('2026-07-07 22:57:39.601473', '2026-07-07 22:57:39.601518', 'e5164ce3b33449bf93e121af4524b081', '2026-07-02', 0, 1, 'Абонемент', 'e229ce3d79d648d9a86a4588ae3b83dd', 'd249d49c51d84363acaf35f2e0e15bc5', NULL, '31cddb9484894e66aa6beefd98a466cc', 'dd99bf01cf634d92974b1aa3f095e02e'),
('2026-07-07 22:58:09.141570', '2026-07-07 22:58:09.141597', 'e8a0513037a84e18b4a50df58b78c1c3', '2026-07-22', 0, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '31cddb9484894e66aa6beefd98a466cc', 'b71942feae48453e9a8b10b8b1bf0286'),
('2026-07-07 22:40:03.880715', '2026-07-07 23:02:14.982832', 'f0f2498decad4a2a8fc92ec316503a3e', '2026-07-06', 1, 1, 'Абонемент', '69c8b06ff95d4e8bb2e7db8f5117cfda', '6d972bc1300f45a49b5533ff5b451adb', NULL, 'e242d081296344ee8236925557a53439', '2ad3a703c37e471e8acd08389e14e623'),
('2026-07-17 08:04:04.843609', '2026-07-17 08:06:44.037858', 'f2134f5c15b3452e8dd7529cedcd4365', '2026-07-16', 1, 1, 'дополнительное', '4bcf75ed7c514f829af369a0b517a42f', NULL, '94e1f559746e431bb86c95f6ce92bcc7', '6400cbcc622f4ccc9417933f597a97f7', NULL),
('2026-07-07 22:36:51.361715', '2026-07-07 23:20:19.972459', 'fb0f3fbdf871445ab447a44de1c8d789', '2026-07-01', 1, 1, 'Абонемент', '4bcf75ed7c514f829af369a0b517a42f', 'ce5024544eee49dcb55b5892fc87fbee', NULL, '31cddb9484894e66aa6beefd98a466cc', 'b71942feae48453e9a8b10b8b1bf0286');

-- --------------------------------------------------------

--
-- Структура таблицы `core_auditlog`
--

CREATE TABLE `core_auditlog` (
  `id` bigint NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `action` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_centersettings`
--

CREATE TABLE `core_centersettings` (
  `id` bigint NOT NULL,
  `trial_cost` decimal(10,2) NOT NULL,
  `single_cost_multiplier` decimal(4,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_classroom`
--

CREATE TABLE `core_classroom` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `capacity` smallint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_direction`
--

CREATE TABLE `core_direction` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `subscription_cost` decimal(10,2) NOT NULL,
  `single_lesson_cost` decimal(10,2) NOT NULL,
  `min_age` smallint UNSIGNED NOT NULL,
  `max_age` smallint UNSIGNED NOT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lesson_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price_per_lesson` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `core_direction`
--

INSERT INTO `core_direction` (`created_at`, `updated_at`, `id`, `name`, `description`, `subscription_cost`, `single_lesson_cost`, `min_age`, `max_age`, `gender`, `lesson_type`, `price_per_lesson`) VALUES
('2026-07-07 21:11:35.646242', '2026-07-07 21:11:35.646242', '0ac197ca71fa4600a6648865d90de501', 'Мастерская чудес', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.686409', '2026-07-07 21:11:35.686409', '0ae8ee156ceb4d6a88896248c137dc7a', 'Увлекательный русский язык (6 класс)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:38:28.702640', '2026-07-07 21:38:28.702679', '1f086e154be447cbacb8d682e5117527', 'Вокал подготовка к конкурсу(Грею счастье)', 'Подготовка к конкурсу', 0.00, 800.00, 3, 18, '', 'group', 450.00),
('2026-07-07 21:11:35.589992', '2026-07-07 21:11:35.589992', '21ec1132c8954073a04e7c6ec730587c', 'Студия живописи и творчества \"Юный Пикассо\" с 7 лет', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:36.137622', '2026-07-07 21:11:36.137622', '25509136a4cd4105ba3c39d035054d53', 'Студия \"Радуга знаний\" (3-5 лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.669207', '2026-07-07 21:11:35.669207', '29deace8cd814482a82c60ea04f6ad6a', 'Студия творчества \"Искусница\"', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.636164', '2026-07-07 21:11:35.636164', '3227229e245f4022bb4d97644bb5755a', 'Логопедические занятия', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.767915', '2026-07-07 21:11:35.767915', '369f5d9170b845bcbe28dfeb5093aa3d', 'Курс \"Юные биологи\" (5-8 кл)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.653808', '2026-07-07 21:11:35.653808', '3d6c60947bfa44bab790d1fa35b8b92b', 'Студия лепки с 5 лет', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.627993', '2026-07-07 21:11:35.627993', '45848cc6b2cd4ca2b5f86f72e4492e26', 'Курс \"Ты - общество. Просто о важном\"          (14-17 лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.557460', '2026-07-07 22:56:31.037003', '4bcf75ed7c514f829af369a0b517a42f', 'Вокальная студия \"Творческий пульс\" с 9 лет', 'Импорт из старой CRM', 0.00, 800.00, 3, 18, '', 'group', 450.00),
('2026-07-07 21:11:35.604109', '2026-07-07 21:11:35.604109', '57aba4fdf1ed43b786d45a95cef0edd8', 'Индивидуальные занятия по русскому языку', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'individual', 0.00),
('2026-07-07 21:11:35.614888', '2026-07-07 21:11:35.614888', '5b53e33b6175457fb386c91ff5ee3726', 'Занимательный французский', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.648247', '2026-07-07 21:11:35.648247', '629fc477cabd4bc9a7e19d24535201e1', 'Арт-фантазия', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.571317', '2026-07-07 21:11:35.571317', '62af5fbeb8bc4bc6a9e367e2ec65b943', 'Индивидуальные занятия по математике', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'individual', 0.00),
('2026-07-07 21:11:36.032407', '2026-07-07 21:11:36.032407', '66d60493f2c446a58775b8804407dd47', 'Занимательный английский (Дошкольники)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:37:26.418181', '2026-07-07 21:37:26.418222', '69c8b06ff95d4e8bb2e7db8f5117cfda', 'Вокал подготовка к конкурсу(Родина моя)', 'Подготовка к конкурсу', 0.00, 800.00, 3, 18, '', 'group', 450.00),
('2026-07-07 21:11:35.578905', '2026-07-07 21:11:35.578905', '6b143664f8474029b4427ee98783aa6b', 'Программирование \"Проги Дарования\" с 11 лет', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.566541', '2026-07-07 21:11:35.566541', '8ef8c9b68a8e4c55b6eba82db6c1332b', 'Вокально-инструментальный ансамбль \"Мелодия сердца\" (с 11 лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.686409', '2026-07-07 21:11:35.686409', '95ed54416acb4e7fa4dd5d50ee1c77d0', 'Увлекательная математика (6 класс)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:36.113423', '2026-07-07 21:11:36.113423', '9d2d8cd3cb9c41e6bfb0d46cb923ad6e', 'Занимательный английский (5-7 лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.571317', '2026-07-07 21:11:35.571317', '9ebac65a5cc046f8a67274ee04397fec', 'Индивидуальные занятия по гитаре', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'individual', 0.00),
('2026-07-07 21:11:35.630145', '2026-07-07 21:11:35.630145', 'a3d53d84b752456f9397f16789d763b6', 'Курс \"Машина времени: приключения в прошлое\" (5-7 кл)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:36.074330', '2026-07-07 21:11:36.074330', 'af0ade6f3b06422c88f5b7ec9e32801a', 'Индивидуальные занятия по чтению', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'individual', 0.00),
('2026-07-07 21:11:36.251157', '2026-07-07 21:11:36.251157', 'b5241a758bbd4033ac188cb19dfcf438', 'Занимательный английский (2, 4  класс)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.916094', '2026-07-07 21:11:35.916094', 'bf46ae5f2cd846189b654e65ea0d3d8e', 'Студия рисования Мастерская чудес (4-6 лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.735554', '2026-07-07 21:11:35.735554', 'c359439deb0d4ae9a410fdcf40a0b27a', 'HIP-HOP (7лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.578905', '2026-07-07 21:11:35.578905', 'c53cbd288dec450bb9e219c5567c09f7', 'Увлекательная математика', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.638910', '2026-07-07 21:11:35.638910', 'ccbbcf64dfa84112861e369023e7c209', 'Речевая студия \"Говоруша\" (3-5 лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.711384', '2026-07-07 21:51:44.942577', 'd1d689b78d954324a31744f31cf4af7a', '\"Скоро в школу\" (5-6 лет)', 'редакция', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.776291', '2026-07-07 21:11:35.776291', 'dce7710b06234ff8b8bb310da93c2d04', 'Занимательный английский (6 класс)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 22:18:29.460891', '2026-07-07 22:18:29.460963', 'e229ce3d79d648d9a86a4588ae3b83dd', 'Индивидуальные занятия по вокалу', '', 3200.00, 1000.00, 3, 18, '', 'individual', 800.00),
('2026-07-07 21:11:35.891891', '2026-07-07 21:11:35.891891', 'f74592c203d340fcae06c52c7a17c733', 'Студия творчества Арт-фантазия (с 7 лет)', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.562206', '2026-07-07 21:11:35.562206', 'faf8c1a10bc24bc0bb122f07eb1a032a', 'Вокальная студия с 4 лет', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'group', 0.00),
('2026-07-07 21:11:35.619962', '2026-07-07 21:11:35.619962', 'ffcb712a49ec43638fdbab9887ac0c56', 'Индивидуальные занятия по английскому языку', 'Импорт из старой CRM', 0.00, 500.00, 3, 12, '', 'individual', 0.00);

-- --------------------------------------------------------

--
-- Структура таблицы `core_kanbantask`
--

CREATE TABLE `core_kanbantask` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `assignee_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_materialpurchase`
--

CREATE TABLE `core_materialpurchase` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `quantity` int UNSIGNED NOT NULL,
  `unit_cost` decimal(10,2) NOT NULL,
  `total_cost` decimal(10,2) NOT NULL,
  `purchase_date` date NOT NULL,
  `supplier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_newsitem`
--

CREATE TABLE `core_newsitem` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `published_date` date NOT NULL,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_parent`
--

CREATE TABLE `core_parent` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_parent`
--

INSERT INTO `core_parent` (`created_at`, `updated_at`, `id`, `name`, `phone`, `email`) VALUES
('2026-07-07 21:11:35.878446', '2026-07-07 21:11:35.878446', '0718be8b411644d5bb003d2d7b236abc', 'Людмила', '+79177285443', ''),
('2026-07-07 21:11:36.389163', '2026-07-07 21:11:36.389163', '07d3b829eb8147878d7aafd1dd6501ba', 'Ирина Васильевна', '8-927-524-44-46', ''),
('2026-07-07 21:11:36.310337', '2026-07-07 21:11:36.310337', '0d08cc7cdd34442ea469a8b1a1fd12bf', 'Анна Валерьевна', '89377005490', ''),
('2026-07-07 21:11:36.267697', '2026-07-07 21:11:36.267697', '1205aab038f74602b6bc05088eb8377a', 'Юлия Юрьевна', '8-961-081-00-73', ''),
('2026-07-07 21:11:36.405247', '2026-07-07 21:11:36.405247', '120a4ca4ec374832a84ddc0771383839', 'Любовь Сергеевна', '8 904-426-83-32', ''),
('2026-07-07 21:11:36.252439', '2026-07-07 21:11:36.252439', '13a784a9aabe4779bdf09840c10b180e', 'Лидия Владимировна', '89190672354', ''),
('2026-07-07 21:11:36.099106', '2026-07-07 21:11:36.099106', '18793673c7134d6a97bd1c4a22118dd6', 'Мария', '89182101778', ''),
('2026-07-07 21:11:36.149389', '2026-07-07 21:11:36.149389', '1e43dedcc6dc4bd3a6b672ff76937ae7', 'Елена', '89177275047', ''),
('2026-07-07 21:11:35.901533', '2026-07-07 21:11:35.901533', '32047aa1e6714eb78c016b2751f2ae90', 'Дарья Дмитриевна', '89891658033', ''),
('2026-07-07 21:11:35.759506', '2026-07-07 22:05:10.226626', '3596bd683fb1486f9a62beee47a91f50', 'Наталья Владимировна', '9608893230', ''),
('2026-07-07 21:11:36.064829', '2026-07-07 21:11:36.064829', '35e1028fd8fe4ecaa10a2e121b95bd60', 'Михаил', '89375427528', ''),
('2026-07-07 21:11:36.348288', '2026-07-07 21:11:36.348288', '380b8f58cdb7455f9834a88d00eedba1', 'Владислава Сергеевна', '8 906-405-60-02, 8 927-513-39-02', ''),
('2026-07-07 21:11:36.356950', '2026-07-07 21:11:36.356950', '399f14c0541f479fb5fc1f2c9771821a', 'Олеся Геннадьевна', '8-905-330-32-89', ''),
('2026-07-07 21:11:36.040318', '2026-07-07 21:11:36.040318', '3f83e3182f874404b7366af42d683b23', 'Родитель Аргунова Настя', '', ''),
('2026-07-07 21:11:36.330110', '2026-07-07 21:11:36.330110', '45b00316bbe4414dbba1b92e4a2e625e', 'Анастасия Владимировна', '8-917-845-89-53', ''),
('2026-07-07 21:11:36.145795', '2026-07-07 21:11:36.259512', '4b1a2cae466049d3b3ca935d25e97998', 'Валерия Константиновна', '89033743869', ''),
('2026-07-07 21:11:36.229148', '2026-07-07 21:11:36.229148', '4dba099c971249d3865fbd9e18b7a497', 'Анна Александровна', '89610664449', ''),
('2026-07-07 21:11:36.372943', '2026-07-07 21:11:36.372943', '5731d2c7a50e42bb9ab3774af47ce569', 'Дарья Александровна', '89371013999', ''),
('2026-07-07 21:11:36.006878', '2026-07-07 21:11:36.006878', '5d811224228642fc9db4806f25fa6431', 'Жанна Геннадьевна', '89876511155', ''),
('2026-07-07 21:11:36.135474', '2026-07-07 21:11:36.135474', '632c6b0513834046b5037f3beec62628', 'Наталья', '89047730970', ''),
('2026-07-07 21:11:36.296465', '2026-07-07 21:11:36.296465', '645d09e1897544a9985973786e221457', 'Надежда Павловна', '89275373537', ''),
('2026-07-07 21:11:35.973003', '2026-07-07 21:11:35.973003', '6b9a9923d39c4e07b238a4c83769af50', 'Юлия Андреевна', '89914217979', ''),
('2026-07-07 21:11:36.210906', '2026-07-07 21:11:36.210906', '6f1d4b87ad1645bd8d66d1cc09b531d7', 'Александра Юрьевна', '89176408375', ''),
('2026-07-07 21:11:36.454849', '2026-07-07 21:11:36.454849', '6f22757bdd714aa0b1e4b1bc47e6fc09', 'Родитель', '8 902-450-44-99', ''),
('2026-07-07 21:11:35.866564', '2026-07-07 21:11:35.866564', '730111a667a24fe386115325156107b4', 'Виктория', '+79616605597', ''),
('2026-07-07 21:11:36.047637', '2026-07-07 21:11:36.047637', '73464a76949d47598c6cca8c0ef7fcda', 'Наталья Ильясовна', '89275218081', ''),
('2026-07-07 21:11:36.288782', '2026-07-07 21:11:36.288782', '792991eaf4cc4d97a9bf9c0fadaeaad6', 'Марина Сергеевна', '89649155608', ''),
('2026-07-07 21:11:36.121468', '2026-07-07 21:11:36.121468', '7b989a48b1ee4f9e8937cd451c3052d6', 'Анастасия', '89176498969', ''),
('2026-07-07 21:11:35.718084', '2026-07-07 21:11:35.718084', '7e1df37c78c6437b8150a24db20d1ad4', 'Юлия Михайловна', '89526952026', ''),
('2026-07-07 21:11:36.465095', '2026-07-07 21:11:36.465095', '7ed14d6567a04d27a0c2af05ccfd07f2', 'Ольга Александровна', '8 960-875-00-03', ''),
('2026-07-07 21:11:35.940749', '2026-07-07 21:11:35.940749', '89eb309fd5fc42ee87a0bb2f41fb9c8e', 'Татьяна Сергеевна', '89275220515', ''),
('2026-07-07 21:11:35.997879', '2026-07-07 21:11:35.997879', '8beaa8b7a9044739a0ad538fd0016e65', 'Светлана Владимировна', '8 909-391-18-82', ''),
('2026-07-07 21:11:36.437917', '2026-07-07 21:11:36.437917', '9bb1a981193e42029a33544be1e961cb', 'Ирина Александровна', '8 9034784288', ''),
('2026-07-07 21:11:36.275717', '2026-07-07 21:11:36.275717', '9dbca8c36c2f4210aa174419b5a70d88', 'Олеся Геннадьевна', '89053303289', ''),
('2026-07-07 21:11:36.242892', '2026-07-07 21:11:36.242892', '9e02375f81d847a28e57d74bcf6e55ab', 'Алина Сергеевна', '89064041492', ''),
('2026-07-07 21:11:35.706846', '2026-07-07 21:11:35.706846', '9fe597a5c2d541238b146d66a1c969c3', 'Татьяна Николаевна', '89667892118', ''),
('2026-07-07 21:11:35.826265', '2026-07-07 21:11:35.826265', 'a75d12f36044481f94e81a56e2617d50', 'Елена Константиновна', '+79047596324', ''),
('2026-07-07 21:11:36.446128', '2026-07-07 22:17:08.378329', 'a9338b545c2b4561bbb3e53fd38dcb23', 'Юлия', '8-961-082-70-27', ''),
('2026-07-07 21:11:36.093488', '2026-07-07 21:11:36.093488', 'a9f89578e99e4b45baaae9e49b7e74d8', 'Алина Александровна', '89270688949', ''),
('2026-07-07 21:11:36.414230', '2026-07-07 22:17:33.122072', 'ae54be6f737a409db753b80285ac2965', 'Юлия Николаевна', '8 961-065-22-67', ''),
('2026-07-07 21:11:35.932564', '2026-07-07 21:11:35.932564', 'aeb9224bd2df4f008658dceb4fb5af12', 'Людмила Ивановна', '89177285443', ''),
('2026-07-07 21:11:36.074330', '2026-07-07 21:11:36.074330', 'b00593ec23af4b9d818a8c2d09c6488d', 'Оксана Сергеевна', '89093831917', ''),
('2026-07-07 21:11:35.801077', '2026-07-07 21:11:35.801077', 'b54a83d6328b429b83c4566249354292', 'Наталия Викторовна', '89053348294', ''),
('2026-07-07 21:11:36.478992', '2026-07-07 21:11:36.478992', 'b563c274f1264479a4d9f58f85ad6800', 'Диана Алишеровна', '8 950-020-12-61', ''),
('2026-07-07 21:11:35.711384', '2026-07-07 21:11:35.711384', 'b573df4514fc43159b041164c0c2d017', 'Юлия Александровна', '89275254577', ''),
('2026-07-07 21:11:35.981225', '2026-07-07 21:11:35.981225', 'b5d0354706614c099c58301ecd1748ea', 'Татьяна Александровна', '89696507053', ''),
('2026-07-07 21:11:35.849820', '2026-07-07 21:11:35.849820', 'b6ae086ccbde44238ac28978becdd892', 'Мкртчян Ануш', '+79627618174', ''),
('2026-07-07 21:11:35.951264', '2026-07-07 21:11:35.951264', 'bb41a5e98f5f43cb835bcc4200cc3185', 'Виктория Вадимовна', '89610910111', ''),
('2026-07-07 21:11:35.795985', '2026-07-07 21:11:35.795985', 'bcf95ed3271c4ba4a716e5084fb8c799', 'Ксения Леонидовна', '89118522513', ''),
('2026-07-07 21:11:36.424230', '2026-07-07 21:11:36.424230', 'c0a6a167d6164e8f9f5cb2e6c86d4373', 'Юлия', '89610827027', ''),
('2026-07-07 21:11:35.997879', '2026-07-07 21:11:35.997879', 'c72f530bc1cc47a6a5c724a84d20c862', 'Анна Сергеевна', '89064044411', ''),
('2026-07-07 21:11:35.743126', '2026-07-07 21:11:35.743126', 'cb2003a5867943a49b2142171afe6ad2', 'Светлана Никаноровна', '89061703070', ''),
('2026-07-07 21:11:35.916094', '2026-07-07 21:11:35.916094', 'ce5a63a08a454902b35548b87cec3f0d', 'Екатерина Юрьевна', '89272580945', ''),
('2026-07-07 21:11:35.963168', '2026-07-07 21:11:35.963168', 'd2a680a553ad4921a13846cee12faf59', 'Ксения Сергеевна', '89053309643', ''),
('2026-07-07 21:11:36.430448', '2026-07-07 21:11:36.430448', 'd4ed789c35db4b8287a25fd2f77fc24b', 'Александра Олеговна', '8 9093938832', ''),
('2026-07-07 21:11:36.304296', '2026-07-07 21:11:36.304296', 'dba9a6b5adb94f36a66f58f3d90718da', 'Юлия', '8 906 165 6756', ''),
('2026-07-07 21:11:35.912073', '2026-07-07 21:11:35.912073', 'dc18b16c6e0e4a6bbd17e2eecc1db0d8', 'Денис', '89275163333', ''),
('2026-07-07 21:11:36.105294', '2026-07-07 21:11:36.105294', 'dd0d5dea6cb347bbb8c02ec29588f3ee', 'Марина', '89880058966', ''),
('2026-07-07 21:11:36.365270', '2026-07-07 21:11:36.365270', 'e0c32e82488449e3bd14c52fb4aab86e', 'Наталья Юрьевна', '89608779255', ''),
('2026-07-07 21:11:35.677443', '2026-07-07 21:11:35.677443', 'e7488e71fd6048fb8197493c556a039d', 'Наталья Игоревна', '89275295153', ''),
('2026-07-07 21:11:36.032407', '2026-07-07 21:11:36.032407', 'e82831cc2d2044b5becd5ee43d74b43d', 'Кристина', '89610860707', ''),
('2026-07-07 21:11:35.974692', '2026-07-07 21:11:35.974692', 'e8804de6ba884e629427b71a22e12e61', 'Людмила Сергеевна', '89297858004', ''),
('2026-07-07 21:11:36.184459', '2026-07-07 21:11:36.184459', 'e8c4ecb3dece42589e21726c826e5d81', 'Ксения', '89616719344', ''),
('2026-07-07 21:11:35.841372', '2026-07-07 21:11:35.841372', 'ec988ae8f2be48d7bdb1ff7c7cead2a9', 'Ольга', '+79880347290', ''),
('2026-07-07 21:11:36.056457', '2026-07-07 21:11:36.056457', 'f6d27cb54409476490eb050ad8a2a169', 'Александр', '89610666677', ''),
('2026-07-07 21:11:35.924351', '2026-07-07 21:11:35.924351', 'fdf4711ab0fc4dbdb99018dd9c52b4c3', 'Наталья Сергеевна', '89275142145', '');

-- --------------------------------------------------------

--
-- Структура таблицы `core_payment`
--

CREATE TABLE `core_payment` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `payment_date` date NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_by_id` int DEFAULT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `student_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_payment`
--

INSERT INTO `core_payment` (`created_at`, `updated_at`, `id`, `payment_date`, `amount`, `payment_type`, `notes`, `created_by_id`, `direction_id`, `student_id`) VALUES
('2026-07-17 08:04:04.845158', '2026-07-17 08:04:04.845194', '02537412a30f4c888528b84c2e8cd26d', '2026-07-16', 450.00, 'other', 'дополнительное', 1, '4bcf75ed7c514f829af369a0b517a42f', '6400cbcc622f4ccc9417933f597a97f7'),
('2026-07-07 23:01:03.314714', '2026-07-17 08:16:59.475864', '128888dfbd7c4851940240a7bcb60518', '2026-07-01', 1600.00, 'subscription', 'Абонемент', 2, '9ebac65a5cc046f8a67274ee04397fec', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-17 08:04:38.479469', '2026-07-17 08:04:38.479492', '148e3f395fc74294a16936bf6141bc84', '2026-07-16', 450.00, 'other', 'дополнительное', 1, '4bcf75ed7c514f829af369a0b517a42f', 'e242d081296344ee8236925557a53439'),
('2026-07-07 22:38:20.168867', '2026-07-07 22:38:20.168890', '4f647e8b2f7740829ccb45cd087bae48', '2026-07-04', 800.00, 'other', 'Разовое занятие', 2, 'e229ce3d79d648d9a86a4588ae3b83dd', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-17 08:02:30.381190', '2026-07-17 08:16:59.457777', '57657c05df924286b3baab066bc5bfde', '2026-07-14', 450.00, 'other', 'дополнительное', 1, '1f086e154be447cbacb8d682e5117527', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 22:58:09.112261', '2026-07-07 22:58:09.112293', '6f7b9b4909184fe1b2d2808b0fa65ffc', '2026-07-08', 1350.00, 'subscription', 'Абонемент', 2, '4bcf75ed7c514f829af369a0b517a42f', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-07 22:56:43.749716', '2026-07-07 23:23:45.740314', '744c97c20ef8423d9b940cae7f81a4d2', '2026-07-01', 1350.00, 'subscription', 'Абонемент', 2, '4bcf75ed7c514f829af369a0b517a42f', '6400cbcc622f4ccc9417933f597a97f7'),
('2026-07-07 23:00:21.928461', '2026-07-17 08:16:59.461472', '798e18ce71ca4f5b90ebec0ec8f788aa', '2026-07-08', 1350.00, 'subscription', 'Абонемент', 2, '4bcf75ed7c514f829af369a0b517a42f', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-17 08:01:45.686953', '2026-07-17 08:01:45.686976', '82171039c31343a5b285698a8b4c39f2', '2026-07-14', 450.00, 'other', 'дополнительное', 1, '1f086e154be447cbacb8d682e5117527', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-07 22:57:39.586875', '2026-07-07 22:59:02.440912', '9eeeb20bfd5844a883362965ac51a1b0', '2026-07-08', 800.00, 'subscription', 'Абонемент', 2, 'e229ce3d79d648d9a86a4588ae3b83dd', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-07 22:58:32.588469', '2026-07-07 22:58:32.588521', 'c6d62378b603441f8c14203847bb70ba', '2026-07-08', 900.00, 'subscription', 'Абонемент', 2, '1f086e154be447cbacb8d682e5117527', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-17 08:05:47.049039', '2026-07-17 08:05:47.049066', 'c98c239f0ae34a16beebd031f5364f01', '2026-07-16', 450.00, 'other', 'дополнительное', 1, '4bcf75ed7c514f829af369a0b517a42f', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-07 22:55:40.767970', '2026-07-07 22:55:40.768002', 'cc326d7b4bf4451a9c7ee6493c2fc502', '2026-07-08', 900.00, 'subscription', 'изменяла', 2, '69c8b06ff95d4e8bb2e7db8f5117cfda', 'e242d081296344ee8236925557a53439'),
('2026-07-07 22:54:16.269136', '2026-07-07 22:54:47.568618', 'cc59a07ed31647e3a58b936f6b8450cb', '2026-07-08', 1350.00, 'subscription', 'Абонемент', 2, '4bcf75ed7c514f829af369a0b517a42f', 'e242d081296344ee8236925557a53439'),
('2026-07-07 22:52:44.828206', '2026-07-07 23:23:32.601662', 'd9afc8db823646b887d9f7b013865c82', '2026-07-01', 900.00, 'subscription', 'Абонемент', 2, '69c8b06ff95d4e8bb2e7db8f5117cfda', '6400cbcc622f4ccc9417933f597a97f7'),
('2026-07-17 08:06:31.089217', '2026-07-17 08:16:59.453616', 'db3c8ba949c443ad9ceac2584be68307', '2026-07-16', 450.00, 'other', 'дополнительное', 1, '4bcf75ed7c514f829af369a0b517a42f', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 23:00:16.121924', '2026-07-17 08:16:59.466453', 'dd0cc0a94c4d490592dfadccf8faa3fc', '2026-07-08', 900.00, 'subscription', 'Абонемент', 2, '69c8b06ff95d4e8bb2e7db8f5117cfda', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 23:00:01.493324', '2026-07-17 08:16:59.471171', 'fda14a47e0554d2497a9a61ec6f072b8', '2026-07-08', 900.00, 'subscription', 'Абонемент', 2, '1f086e154be447cbacb8d682e5117527', 'eac9ac0253564743b6a695fc1af487df');

-- --------------------------------------------------------

--
-- Структура таблицы `core_scheduleexception`
--

CREATE TABLE `core_scheduleexception` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lesson_date` date NOT NULL,
  `exception_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `notes` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `schedule_slot_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `substitute_teacher_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_scheduleslot`
--

CREATE TABLE `core_scheduleslot` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `day_of_week` int NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `is_archived` tinyint(1) NOT NULL,
  `classroom_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `subdirection_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `teacher_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sort_order` int UNSIGNED NOT NULL,
  `student_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `core_scheduleslot`
--

INSERT INTO `core_scheduleslot` (`created_at`, `updated_at`, `id`, `day_of_week`, `start_time`, `end_time`, `is_archived`, `classroom_id`, `direction_id`, `subdirection_id`, `teacher_id`, `sort_order`, `student_id`) VALUES
('2026-07-07 21:40:40.265442', '2026-07-07 21:40:40.265480', '6d972bc1300f45a49b5533ff5b451adb', 0, '19:00:00.000000', '19:45:00.000000', 0, NULL, '69c8b06ff95d4e8bb2e7db8f5117cfda', NULL, '101bdf340d3445999dec2b2f17b6590f', 0, NULL),
('2026-07-07 21:41:04.972061', '2026-07-07 21:41:04.972119', '8274b9a656f74e53bd2aa32e1c86f43b', 1, '17:45:00.000000', '18:30:00.000000', 0, NULL, '1f086e154be447cbacb8d682e5117527', NULL, '101bdf340d3445999dec2b2f17b6590f', 0, NULL),
('2026-07-07 22:08:02.083349', '2026-07-07 22:08:02.083394', '97542447921a4cc6bad0bdb5fc9ce9d4', 1, '18:30:00.000000', '19:15:00.000000', 0, NULL, '9ebac65a5cc046f8a67274ee04397fec', NULL, '101bdf340d3445999dec2b2f17b6590f', 1, 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 21:35:41.217543', '2026-07-07 21:35:41.217565', 'ce5024544eee49dcb55b5892fc87fbee', 2, '19:00:00.000000', '19:45:00.000000', 0, NULL, '4bcf75ed7c514f829af369a0b517a42f', NULL, '101bdf340d3445999dec2b2f17b6590f', 0, NULL),
('2026-07-07 22:36:27.369090', '2026-07-07 22:36:27.369133', 'd249d49c51d84363acaf35f2e0e15bc5', 3, '18:00:00.000000', '18:45:00.000000', 0, NULL, 'e229ce3d79d648d9a86a4588ae3b83dd', NULL, '101bdf340d3445999dec2b2f17b6590f', 0, '31cddb9484894e66aa6beefd98a466cc');

-- --------------------------------------------------------

--
-- Структура таблицы `core_singlelesson`
--

CREATE TABLE `core_singlelesson` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lesson_date` date NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `lesson_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `classroom_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_by_id` int DEFAULT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `student_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_singlelesson`
--

INSERT INTO `core_singlelesson` (`created_at`, `updated_at`, `id`, `lesson_date`, `start_time`, `end_time`, `lesson_type`, `cost`, `notes`, `classroom_id`, `created_by_id`, `direction_id`, `student_id`, `teacher_id`) VALUES
('2026-07-17 08:02:30.378032', '2026-07-17 08:02:30.378091', '0fccbaf00910495cb051a965d5b25e6a', '2026-07-14', '17:15:00.000000', '17:45:00.000000', 'makeup', 450.00, 'дополнительное', NULL, 1, '1f086e154be447cbacb8d682e5117527', 'eac9ac0253564743b6a695fc1af487df', '101bdf340d3445999dec2b2f17b6590f'),
('2026-07-17 08:04:38.476765', '2026-07-17 08:04:38.476798', '1ad50f5a70eb4311ac5a406370572846', '2026-07-16', '18:00:00.000000', '19:00:00.000000', 'makeup', 450.00, 'дополнительное', NULL, 1, '4bcf75ed7c514f829af369a0b517a42f', 'e242d081296344ee8236925557a53439', '101bdf340d3445999dec2b2f17b6590f'),
('2026-07-17 08:05:47.046734', '2026-07-17 08:05:47.046769', '7b938857cbea46ed891db27996bace35', '2026-07-16', '18:00:00.000000', '19:00:00.000000', 'makeup', 450.00, 'дополнительное', NULL, 1, '4bcf75ed7c514f829af369a0b517a42f', '31cddb9484894e66aa6beefd98a466cc', '101bdf340d3445999dec2b2f17b6590f'),
('2026-07-17 08:04:04.841854', '2026-07-17 08:04:04.841900', '94e1f559746e431bb86c95f6ce92bcc7', '2026-07-16', '18:00:00.000000', '19:00:00.000000', 'makeup', 450.00, 'дополнительное', NULL, 1, '4bcf75ed7c514f829af369a0b517a42f', '6400cbcc622f4ccc9417933f597a97f7', '101bdf340d3445999dec2b2f17b6590f'),
('2026-07-07 22:38:20.166853', '2026-07-07 22:38:20.166886', 'd81f562bd50b4ca08cc41402f4ca544a', '2026-07-04', '15:20:00.000000', '16:05:00.000000', 'makeup', 800.00, '', NULL, 2, 'e229ce3d79d648d9a86a4588ae3b83dd', '31cddb9484894e66aa6beefd98a466cc', '101bdf340d3445999dec2b2f17b6590f'),
('2026-07-17 08:06:31.087224', '2026-07-17 08:06:31.087255', 'e4e917f5921d4250adb86ee14758005f', '2026-07-16', '18:00:00.000000', '19:00:00.000000', 'makeup', 450.00, 'дополнительное', NULL, 1, '4bcf75ed7c514f829af369a0b517a42f', 'eac9ac0253564743b6a695fc1af487df', '101bdf340d3445999dec2b2f17b6590f'),
('2026-07-17 08:01:45.681826', '2026-07-17 08:01:45.681857', 'f7bdfe1f6ffd436e8d7f4a407037612e', '2026-07-14', '17:15:00.000000', '17:45:00.000000', 'makeup', 450.00, 'дополнительное', NULL, 1, '1f086e154be447cbacb8d682e5117527', '31cddb9484894e66aa6beefd98a466cc', '101bdf340d3445999dec2b2f17b6590f');

-- --------------------------------------------------------

--
-- Структура таблицы `core_student`
--

CREATE TABLE `core_student` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `registration_date` date NOT NULL,
  `parent_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_student`
--

INSERT INTO `core_student` (`created_at`, `updated_at`, `id`, `name`, `date_of_birth`, `gender`, `notes`, `registration_date`, `parent_id`) VALUES
('2026-07-07 21:11:36.097090', '2026-07-07 21:11:36.097090', '020e008644aa4490a2954618fc4578eb', 'Дудкина Мирослава', '2020-08-05', 'boy', '', '2026-07-08', 'a9f89578e99e4b45baaae9e49b7e74d8'),
('2026-07-07 21:11:36.471574', '2026-07-07 21:11:36.471574', '08e1278fad44442285fe4d205d36a24a', 'Ковалев Алексей', '2017-06-17', 'boy', '', '2026-07-08', '7ed14d6567a04d27a0c2af05ccfd07f2'),
('2026-07-07 21:11:35.841807', '2026-07-07 21:11:35.841807', '0ba670b4693542d58db4f8d28b881db1', 'Багрова Анфиса', '2013-09-08', 'girl', '', '2026-07-08', 'ec988ae8f2be48d7bdb1ff7c7cead2a9'),
('2026-07-07 21:11:36.437917', '2026-07-07 21:11:36.437917', '0ff1d1f19d78453db3fecd074510f0c6', 'Кижаева Алисия', '2023-09-17', 'girl', '', '2026-07-08', 'd4ed789c35db4b8287a25fd2f77fc24b'),
('2026-07-07 21:11:36.405247', '2026-07-07 21:11:36.405247', '10e6602d1b8a40cc844fa9ab59e11486', 'Шейкин Матвей', '2022-07-24', 'boy', 'любит рисование, танцы, пение', '2026-07-08', '120a4ca4ec374832a84ddc0771383839'),
('2026-07-07 21:11:36.259512', '2026-07-07 21:11:36.259512', '1240f8febd704b6583f3f8771be46495', 'Батырь Катя', '2017-10-06', 'girl', '', '2026-07-08', '4b1a2cae466049d3b3ca935d25e97998'),
('2026-07-07 21:11:35.743126', '2026-07-07 21:11:35.743126', '1b61be39757f4b268c228011652fd693', 'Лобасова Екатерина', '2016-06-26', 'girl', '', '2026-07-08', 'cb2003a5867943a49b2142171afe6ad2'),
('2026-07-07 21:11:35.952766', '2026-07-07 21:11:35.952766', '1e07fa8275754f59a185e20e1912f9cc', 'Сенюшкин Иван', '2016-08-16', 'boy', '', '2026-07-08', 'bb41a5e98f5f43cb835bcc4200cc3185'),
('2026-07-07 21:11:36.129608', '2026-07-07 21:11:36.129608', '2543d780a52f46baaa70573ab226e7f4', 'Литвинова Василиса', '2016-02-09', 'girl', '', '2026-07-08', 'd2a680a553ad4921a13846cee12faf59'),
('2026-07-07 21:11:36.023162', '2026-07-07 21:11:36.023162', '280267bf5fdb48fdae0a739a49d33019', 'Попов Никита', '2017-05-17', 'boy', '', '2026-07-08', '5d811224228642fc9db4806f25fa6431'),
('2026-07-07 21:11:36.348288', '2026-07-07 21:11:36.348288', '2d488343f08f4e2f974c327b3ad89ea9', 'Шарабок Виктория', '2019-02-27', 'girl', 'любит разнообразие, лепит, танцует', '2026-07-08', '380b8f58cdb7455f9834a88d00eedba1'),
('2026-07-07 21:11:36.214574', '2026-07-07 21:11:36.214574', '31a64f9fb4654f4ea7c67bc8395e824d', 'Розматов Константин', '2017-06-15', 'boy', '', '2026-07-08', '6f1d4b87ad1645bd8d66d1cc09b531d7'),
('2026-07-07 21:11:36.414230', '2026-07-07 22:17:33.123269', '31cddb9484894e66aa6beefd98a466cc', 'Кузнецова Марьяна', '2013-04-17', 'girl', 'эпилепсия, стеснительная', '2026-07-08', 'ae54be6f737a409db753b80285ac2965'),
('2026-07-07 21:11:35.709848', '2026-07-07 21:11:35.709848', '325e191c7ae849468950708db64705bc', 'Фетисов Сергей', '2019-11-25', 'boy', 'Ф', '2026-07-08', '9fe597a5c2d541238b146d66a1c969c3'),
('2026-07-07 21:11:36.290794', '2026-07-07 21:11:36.290794', '364f0fe92bcb430aaaea8a7a2c71c99e', 'Слепцова Мария', '2014-04-04', 'girl', '', '2026-07-08', '792991eaf4cc4d97a9bf9c0fadaeaad6'),
('2026-07-07 21:11:35.997879', '2026-07-07 21:11:35.997879', '371cb55f3ebe45f5bf0b3fb8077e4547', 'Лемещенко Ярослав', '2018-04-29', 'boy', '', '2026-07-08', 'c72f530bc1cc47a6a5c724a84d20c862'),
('2026-07-07 21:11:36.252439', '2026-07-07 21:11:36.252439', '3c89ab53d23c4b278cd2f022042107bc', 'Бычкова Вероника', '2012-11-12', 'girl', '', '2026-07-08', '13a784a9aabe4779bdf09840c10b180e'),
('2026-07-07 21:11:36.074330', '2026-07-07 21:11:36.074330', '3cbe544b689c47bca0d96f5aabbc7bdd', 'Потапова Анна', '2018-09-13', 'girl', '', '2026-07-08', 'b00593ec23af4b9d818a8c2d09c6488d'),
('2026-07-07 21:11:36.356950', '2026-07-07 21:11:36.356950', '42f84b7b6166462a9b079d8ebf3063d0', 'Артаманова Маша', '2012-11-01', 'girl', '', '2026-07-08', '399f14c0541f479fb5fc1f2c9771821a'),
('2026-07-07 21:11:35.932564', '2026-07-07 21:11:35.932564', '4320bba83114446bafb9230e4b692898', 'Семенова Вика', '2019-10-26', 'girl', '', '2026-07-08', 'aeb9224bd2df4f008658dceb4fb5af12'),
('2026-07-07 21:11:35.718084', '2026-07-07 21:11:35.718084', '48fe61a5a73d41bb91936a05be8fdd6e', 'Шумилина Алена', '2021-03-05', 'girl', '', '2026-07-08', 'b573df4514fc43159b041164c0c2d017'),
('2026-07-07 21:11:35.801077', '2026-07-07 21:11:35.801077', '4a61da2f85d540cf80f5e33b76cba03b', 'Гляделова Вика', '2014-04-10', 'girl', '', '2026-07-08', 'bcf95ed3271c4ba4a716e5084fb8c799'),
('2026-07-07 21:11:36.275717', '2026-07-07 21:11:36.275717', '4ba50c2d36b74ef5952bda8c76cb6186', 'Артаманова Виктория Николаевна', '2016-06-01', 'girl', '', '2026-07-08', '9dbca8c36c2f4210aa174419b5a70d88'),
('2026-07-07 21:11:36.298479', '2026-07-07 21:11:36.298479', '4cee16b5514a488fba81636632deaa53', 'Константин Зубков', '2011-10-05', 'boy', '', '2026-07-08', '645d09e1897544a9985973786e221457'),
('2026-07-07 21:11:35.817162', '2026-07-07 21:11:35.817162', '50f0207677794c7f91ea6b0f4fac094e', 'Лобасов Дима', '2013-09-21', 'boy', '', '2026-07-08', 'cb2003a5867943a49b2142171afe6ad2'),
('2026-07-07 21:11:36.137622', '2026-07-07 21:11:36.137622', '51907d697f6d496b929a90820f3bc255', 'Карпенко Ева', '2021-06-11', 'girl', '', '2026-07-08', '632c6b0513834046b5037f3beec62628'),
('2026-07-07 21:11:35.981225', '2026-07-07 21:11:35.981225', '5651faa95491443a823cccde8d7c67e6', 'Давиденко Варвара', '2017-03-08', 'girl', '', '2026-07-08', 'e8804de6ba884e629427b71a22e12e61'),
('2026-07-07 21:11:36.040318', '2026-07-07 21:11:36.040318', '56f0ee0fc8a04749a74ff8707705ecca', 'Аргунова Настя', '2016-11-14', 'girl', '', '2026-07-08', '3f83e3182f874404b7366af42d683b23'),
('2026-07-07 21:11:36.148788', '2026-07-07 21:11:36.148788', '5cadacc38cb74793bd4ffce4fa4a5ec1', 'Батырь Артем', '2012-11-10', 'boy', '', '2026-07-08', '4b1a2cae466049d3b3ca935d25e97998'),
('2026-07-07 21:11:35.726650', '2026-07-07 21:11:35.726650', '631c18815c904479b0305156c716383d', 'Ключникова Анна', '2019-10-21', 'girl', '', '2026-07-08', '7e1df37c78c6437b8150a24db20d1ad4'),
('2026-07-07 21:11:36.454849', '2026-07-07 22:17:08.379593', '6400cbcc622f4ccc9417933f597a97f7', 'Абраменкова София Денисовна', '2015-11-26', 'girl', '', '2026-07-08', 'a9338b545c2b4561bbb3e53fd38dcb23'),
('2026-07-07 21:11:35.965179', '2026-07-07 21:11:35.965179', '643a6f06fd7547fc9abe0ad0a6adc032', 'Литвинов Егор', '2017-07-06', 'boy', '', '2026-07-08', 'd2a680a553ad4921a13846cee12faf59'),
('2026-07-07 21:11:35.901533', '2026-07-07 21:11:35.901533', '654612b0292f40ce82303d90dcb29ce1', 'Сухорукова Евгения', '2017-10-17', 'girl', '', '2026-07-08', '32047aa1e6714eb78c016b2751f2ae90'),
('2026-07-07 21:11:36.341535', '2026-07-07 21:11:36.341535', '6b2bb85b8eff45f49196aa6d4e2833e0', 'Владимир Леккарев', '2015-05-05', 'boy', 'второй акк', '2026-07-08', '45b00316bbe4414dbba1b92e4a2e625e'),
('2026-07-07 21:11:36.047637', '2026-07-07 21:11:36.047637', '70b088f37a004fcda4c85879774bc2af', 'Попович София', '2020-08-25', 'girl', '', '2026-07-08', '73464a76949d47598c6cca8c0ef7fcda'),
('2026-07-07 21:11:36.064829', '2026-07-07 21:11:36.064829', '72edcfef24774cf8b0e9936a1c14eda9', 'Лысаков Ярослав', '2017-08-10', 'boy', '', '2026-07-08', '35e1028fd8fe4ecaa10a2e121b95bd60'),
('2026-07-07 21:11:36.242892', '2026-07-07 21:11:36.242892', '74ab1798e4ca4ef2b2aba672c9c3d866', 'Панфилов Артем', '2017-08-05', 'boy', '', '2026-07-08', '9e02375f81d847a28e57d74bcf6e55ab'),
('2026-07-07 21:11:36.372943', '2026-07-07 21:11:36.372943', '763cc0c7411647dca273c5e9a7e5f7b3', 'Иванов Максим Вячеславович', '2018-04-23', 'boy', '', '2026-07-08', '1205aab038f74602b6bc05088eb8377a'),
('2026-07-07 21:11:36.198873', '2026-07-07 21:11:36.198873', '7d1fa8023b4549849c81639cce9736c8', 'Ермаков Никита', '2015-05-21', 'boy', '', '2026-07-08', '632c6b0513834046b5037f3beec62628'),
('2026-07-07 21:11:35.940749', '2026-07-07 21:11:35.940749', '82ed5ed14193419e80e1c6a8468ae47c', 'Мсхаладзе Артём', '2016-09-01', 'boy', '', '2026-07-08', '89eb309fd5fc42ee87a0bb2f41fb9c8e'),
('2026-07-07 21:11:35.826265', '2026-07-07 21:11:35.826265', '85205a3d76894084b232d1552278e217', 'Зотова София', '2025-08-31', 'girl', '', '2026-07-08', 'a75d12f36044481f94e81a56e2617d50'),
('2026-07-07 21:11:35.891891', '2026-07-07 21:11:35.891891', '88a05c0b381a4b62badd546faf2c7127', 'Ростовская Алиса', '2018-10-06', 'girl', '', '2026-07-08', 'b54a83d6328b429b83c4566249354292'),
('2026-07-07 21:11:36.231836', '2026-07-07 21:11:36.231836', '8e7801a5c702410287050f2aaff3ae7a', 'Дегтянникова Амелия', '2022-07-12', 'girl', '', '2026-07-08', '4dba099c971249d3865fbd9e18b7a497'),
('2026-07-07 21:11:35.883193', '2026-07-07 21:11:35.883193', '90a8d548e05445aeacec076364e55251', 'Семёнова Алиса', '2013-09-10', 'girl', '', '2026-07-08', '0718be8b411644d5bb003d2d7b236abc'),
('2026-07-07 21:11:36.121468', '2026-07-07 21:11:36.121468', '96624edaba724405bcffce79852ae7e6', 'Чесноков Мирослав', '2022-10-28', 'boy', '', '2026-07-08', '7b989a48b1ee4f9e8937cd451c3052d6'),
('2026-07-07 21:11:35.924351', '2026-07-07 21:11:35.924351', '99064bceef424e709be6daf8f3d05319', 'Тюфяков Егор', '2015-08-30', 'boy', '', '2026-07-08', 'ce5a63a08a454902b35548b87cec3f0d'),
('2026-07-07 21:11:35.858162', '2026-07-07 21:11:35.858162', '9b04d409bbe843c5919a4730e18beee2', 'Мкртчян Арен', '2014-01-20', 'boy', '', '2026-07-08', 'b6ae086ccbde44238ac28978becdd892'),
('2026-07-07 21:11:36.381660', '2026-07-07 21:11:36.381660', '9b4cd6776bf84e64bba850d1438dc945', 'Каныгина Василиса', '2018-07-20', 'girl', 'ценят грамотную речь', '2026-07-08', '5731d2c7a50e42bb9ab3774af47ce569'),
('2026-07-07 21:11:36.399356', '2026-07-07 21:11:36.399356', 'a5807395318545eba1419336db746d06', 'Крюков Матвей', '2015-03-20', 'boy', '', '2026-07-08', '8beaa8b7a9044739a0ad538fd0016e65'),
('2026-07-07 21:11:36.015243', '2026-07-07 21:11:36.015243', 'a58e61d0a2864bb5a890e784506dd237', 'Попова Милана', '2019-05-08', 'girl', '', '2026-07-08', '5d811224228642fc9db4806f25fa6431'),
('2026-07-07 21:11:36.032407', '2026-07-07 21:11:36.032407', 'a7760ff956c2427d99948ed27445b033', 'Пираева Теона', '2020-08-30', 'girl', '', '2026-07-08', 'e82831cc2d2044b5becd5ee43d74b43d'),
('2026-07-07 21:11:36.105294', '2026-07-07 21:11:36.105294', 'aa52280d9418494e8c3007e750656aa2', 'Нидзий Михаил', '2021-07-31', 'boy', '', '2026-07-08', 'dd0d5dea6cb347bbb8c02ec29588f3ee'),
('2026-07-07 21:11:36.389163', '2026-07-07 21:11:36.389163', 'aaaf11eb3e2447bead153951e2c2f550', 'Отмашкина Инна', '2022-08-08', 'girl', '', '2026-07-08', '07d3b829eb8147878d7aafd1dd6501ba'),
('2026-07-07 21:11:36.153897', '2026-07-07 21:11:36.153897', 'ab32c3716fee46c09e1851bac41ca383', 'Дубягина Милена', '2015-05-01', 'girl', '', '2026-07-08', '1e43dedcc6dc4bd3a6b672ff76937ae7'),
('2026-07-07 21:11:36.446128', '2026-07-07 21:11:36.446128', 'aea8e8871b9f4f2c9eeb05cc8baeb879', 'Давыденко Анна', '2020-02-07', 'girl', '', '2026-07-08', '9bb1a981193e42029a33544be1e961cb'),
('2026-07-07 21:11:35.810038', '2026-07-07 21:11:35.810038', 'aef34071770a4e1780b4531e779df484', 'Ростовская Арина', '2015-06-24', 'girl', '', '2026-07-08', 'b54a83d6328b429b83c4566249354292'),
('2026-07-07 21:11:36.463078', '2026-07-07 21:11:36.463078', 'afffe5372eb8463d980d71baa9f7b13a', 'Бочкарева Вероника', '2019-09-25', 'girl', '', '2026-07-08', '6f22757bdd714aa0b1e4b1bc47e6fc09'),
('2026-07-07 21:11:35.914085', '2026-07-07 21:11:35.914085', 'b0e2208a3a684ca3a093ff13d2c17771', 'Манаенко Арина', '2022-04-06', 'girl', '', '2026-07-08', 'dc18b16c6e0e4a6bbd17e2eecc1db0d8'),
('2026-07-07 21:11:35.866564', '2026-07-07 21:11:35.866564', 'b2e9686da65e43a7bba2450b208c3a12', 'Ермилова София', '2016-01-27', 'girl', '', '2026-07-08', '730111a667a24fe386115325156107b4'),
('2026-07-07 21:11:36.006878', '2026-07-07 21:11:36.006878', 'b5d1a44a6b194d369d68e8af16211ad9', 'Ластовская Надя', '2012-06-28', 'girl', '', '2026-07-08', '8beaa8b7a9044739a0ad538fd0016e65'),
('2026-07-07 21:11:35.924351', '2026-07-07 21:11:35.924351', 'b5ecdfdd51f645589b7a53963e90655f', 'Миссарова Дарина', '2017-12-12', 'girl', '', '2026-07-08', 'fdf4711ab0fc4dbdb99018dd9c52b4c3'),
('2026-07-07 21:11:36.332487', '2026-07-07 21:11:36.332487', 'beaf07ebd2594e9997724bbcf3609d4b', 'Ева Леккарева', '2017-07-16', 'girl', 'второй акк', '2026-07-08', '45b00316bbe4414dbba1b92e4a2e625e'),
('2026-07-07 21:11:36.190295', '2026-07-07 21:11:36.190295', 'c01d415a4d234d0082b99adeba212da6', 'Николаев Илья', '2012-01-16', 'boy', '', '2026-07-08', 'e8c4ecb3dece42589e21726c826e5d81'),
('2026-07-07 21:11:35.685529', '2026-07-07 21:11:35.685529', 'c0a77febed5a4416b7b4c822f1121d8e', 'Попов Давид', '2013-08-25', 'boy', '', '2026-07-08', 'e7488e71fd6048fb8197493c556a039d'),
('2026-07-07 21:11:36.274203', '2026-07-07 21:11:36.274203', 'c897be2190ee4e30b40f9ca42fda908f', 'Иванова Виктория Вячеславовна', '2018-04-23', 'girl', '', '2026-07-08', '1205aab038f74602b6bc05088eb8377a'),
('2026-07-07 21:11:36.306308', '2026-07-07 21:11:36.306308', 'c8d1d505765e46e0af0d1b8b62a41255', 'Фролова Полина', '2015-01-15', 'girl', '', '2026-07-08', 'dba9a6b5adb94f36a66f58f3d90718da'),
('2026-07-07 21:11:35.866564', '2026-07-07 21:11:35.866564', 'c9d6d2d791284cfaaf2be965a577fc3c', 'Мкртчян Ева', '2019-06-04', 'girl', '', '2026-07-08', 'b6ae086ccbde44238ac28978becdd892'),
('2026-07-07 21:11:35.974692', '2026-07-07 21:11:35.974692', 'cccc8f71d218464887606c9808e772f8', 'Терехова Арина', '2021-08-26', 'girl', '', '2026-07-08', '6b9a9923d39c4e07b238a4c83769af50'),
('2026-07-07 21:11:36.105294', '2026-07-07 21:11:36.105294', 'd07061a20bc048d980f30fe107ae2d86', 'Родионов Илья', '2013-09-01', 'boy', '', '2026-07-08', '18793673c7134d6a97bd1c4a22118dd6'),
('2026-07-07 21:11:36.088986', '2026-07-07 21:11:36.088986', 'e242d081296344ee8236925557a53439', 'Куликова Даша', '2018-04-13', 'girl', '', '2026-07-08', 'b5d0354706614c099c58301ecd1748ea'),
('2026-07-07 21:11:35.990446', '2026-07-07 21:11:35.990446', 'e38d58227f21416d8ae5eb0fd9ce46ab', 'Шаповалова София', '2011-02-25', 'girl', '', '2026-07-08', 'b5d0354706614c099c58301ecd1748ea'),
('2026-07-07 21:11:35.759506', '2026-07-07 22:05:10.227965', 'eac9ac0253564743b6a695fc1af487df', 'Тарасова Есения', '2013-02-01', 'girl', '', '2026-07-08', '3596bd683fb1486f9a62beee47a91f50'),
('2026-07-07 21:11:36.056457', '2026-07-07 21:11:36.056457', 'f0677ffadc474b3da6f87e908efbc287', 'Шевченко Марфа', '2017-04-25', 'girl', '', '2026-07-08', 'f6d27cb54409476490eb050ad8a2a169'),
('2026-07-07 21:11:36.367286', '2026-07-07 21:11:36.367286', 'f1cbe8baa61a4b4db8dcb8af87c7a9a1', 'Медведева Александра', '2017-08-26', 'girl', '', '2026-07-08', 'e0c32e82488449e3bd14c52fb4aab86e'),
('2026-07-07 21:11:36.478992', '2026-07-07 21:11:36.478992', 'f28d0c8617a14ec6b812b7624a785b27', 'Шахназаров Мухамед Али', '2022-07-24', 'boy', '', '2026-07-08', 'b563c274f1264479a4d9f58f85ad6800'),
('2026-07-07 21:11:36.316311', '2026-07-07 21:11:36.316311', 'fe42e5def87f45fcabf6ad7361fd812b', 'Аверина Юлия', '2018-06-18', 'girl', '', '2026-07-08', '0d08cc7cdd34442ea469a8b1a1fd12bf');

-- --------------------------------------------------------

--
-- Структура таблицы `core_student_directions`
--

CREATE TABLE `core_student_directions` (
  `id` bigint NOT NULL,
  `student_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_student_directions`
--

INSERT INTO `core_student_directions` (`id`, `student_id`, `direction_id`) VALUES
(240, '1240f8febd704b6583f3f8771be46495', '29deace8cd814482a82c60ea04f6ad6a'),
(144, '1b61be39757f4b268c228011652fd693', '21ec1132c8954073a04e7c6ec730587c'),
(222, '2543d780a52f46baaa70573ab226e7f4', '21ec1132c8954073a04e7c6ec730587c'),
(223, '2543d780a52f46baaa70573ab226e7f4', '29deace8cd814482a82c60ea04f6ad6a'),
(252, '2d488343f08f4e2f974c327b3ad89ea9', '21ec1132c8954073a04e7c6ec730587c'),
(253, '2d488343f08f4e2f974c327b3ad89ea9', 'c359439deb0d4ae9a410fdcf40a0b27a'),
(274, '31cddb9484894e66aa6beefd98a466cc', '1f086e154be447cbacb8d682e5117527'),
(262, '31cddb9484894e66aa6beefd98a466cc', '4bcf75ed7c514f829af369a0b517a42f'),
(275, '31cddb9484894e66aa6beefd98a466cc', 'e229ce3d79d648d9a86a4588ae3b83dd'),
(134, '325e191c7ae849468950708db64705bc', 'd1d689b78d954324a31744f31cf4af7a'),
(213, '3cbe544b689c47bca0d96f5aabbc7bdd', '21ec1132c8954073a04e7c6ec730587c'),
(212, '3cbe544b689c47bca0d96f5aabbc7bdd', 'af0ade6f3b06422c88f5b7ec9e32801a'),
(189, '4320bba83114446bafb9230e4b692898', '3d6c60947bfa44bab790d1fa35b8b92b'),
(224, '51907d697f6d496b929a90820f3bc255', '25509136a4cd4105ba3c39d035054d53'),
(195, '5651faa95491443a823cccde8d7c67e6', '3d6c60947bfa44bab790d1fa35b8b92b'),
(196, '5651faa95491443a823cccde8d7c67e6', '5b53e33b6175457fb386c91ff5ee3726'),
(198, '5651faa95491443a823cccde8d7c67e6', 'c359439deb0d4ae9a410fdcf40a0b27a'),
(207, '56f0ee0fc8a04749a74ff8707705ecca', 'f74592c203d340fcae06c52c7a17c733'),
(226, '5cadacc38cb74793bd4ffce4fa4a5ec1', '95ed54416acb4e7fa4dd5d50ee1c77d0'),
(136, '631c18815c904479b0305156c716383d', '21ec1132c8954073a04e7c6ec730587c'),
(139, '631c18815c904479b0305156c716383d', '3d6c60947bfa44bab790d1fa35b8b92b'),
(142, '631c18815c904479b0305156c716383d', 'c359439deb0d4ae9a410fdcf40a0b27a'),
(138, '631c18815c904479b0305156c716383d', 'ccbbcf64dfa84112861e369023e7c209'),
(267, '6400cbcc622f4ccc9417933f597a97f7', '4bcf75ed7c514f829af369a0b517a42f'),
(273, '6400cbcc622f4ccc9417933f597a97f7', '69c8b06ff95d4e8bb2e7db8f5117cfda'),
(182, '654612b0292f40ce82303d90dcb29ce1', '21ec1132c8954073a04e7c6ec730587c'),
(250, '6b2bb85b8eff45f49196aa6d4e2833e0', 'b5241a758bbd4033ac188cb19dfcf438'),
(208, '70b088f37a004fcda4c85879774bc2af', 'bf46ae5f2cd846189b654e65ea0d3d8e'),
(210, '72edcfef24774cf8b0e9936a1c14eda9', '3227229e245f4022bb4d97644bb5755a'),
(237, '74ab1798e4ca4ef2b2aba672c9c3d866', 'b5241a758bbd4033ac188cb19dfcf438'),
(256, '763cc0c7411647dca273c5e9a7e5f7b3', '21ec1132c8954073a04e7c6ec730587c'),
(179, '88a05c0b381a4b62badd546faf2c7127', '21ec1132c8954073a04e7c6ec730587c'),
(180, '88a05c0b381a4b62badd546faf2c7127', '29deace8cd814482a82c60ea04f6ad6a'),
(178, '88a05c0b381a4b62badd546faf2c7127', '3d6c60947bfa44bab790d1fa35b8b92b'),
(181, '88a05c0b381a4b62badd546faf2c7127', 'f74592c203d340fcae06c52c7a17c733'),
(235, '8e7801a5c702410287050f2aaff3ae7a', 'bf46ae5f2cd846189b654e65ea0d3d8e'),
(177, '90a8d548e05445aeacec076364e55251', '8ef8c9b68a8e4c55b6eba82db6c1332b'),
(221, '96624edaba724405bcffce79852ae7e6', 'bf46ae5f2cd846189b654e65ea0d3d8e'),
(186, '99064bceef424e709be6daf8f3d05319', '3d6c60947bfa44bab790d1fa35b8b92b'),
(205, 'a7760ff956c2427d99948ed27445b033', '66d60493f2c446a58775b8804407dd47'),
(220, 'aa52280d9418494e8c3007e750656aa2', '3227229e245f4022bb4d97644bb5755a'),
(219, 'aa52280d9418494e8c3007e750656aa2', '9d2d8cd3cb9c41e6bfb0d46cb923ad6e'),
(218, 'aa52280d9418494e8c3007e750656aa2', 'bf46ae5f2cd846189b654e65ea0d3d8e'),
(227, 'ab32c3716fee46c09e1851bac41ca383', 'c359439deb0d4ae9a410fdcf40a0b27a'),
(266, 'aea8e8871b9f4f2c9eeb05cc8baeb879', '3d6c60947bfa44bab790d1fa35b8b92b'),
(161, 'aef34071770a4e1780b4531e779df484', '21ec1132c8954073a04e7c6ec730587c'),
(162, 'aef34071770a4e1780b4531e779df484', '29deace8cd814482a82c60ea04f6ad6a'),
(160, 'aef34071770a4e1780b4531e779df484', '3d6c60947bfa44bab790d1fa35b8b92b'),
(163, 'aef34071770a4e1780b4531e779df484', 'c359439deb0d4ae9a410fdcf40a0b27a'),
(268, 'afffe5372eb8463d980d71baa9f7b13a', 'c359439deb0d4ae9a410fdcf40a0b27a'),
(183, 'b0e2208a3a684ca3a093ff13d2c17771', 'bf46ae5f2cd846189b654e65ea0d3d8e'),
(173, 'b2e9686da65e43a7bba2450b208c3a12', '21ec1132c8954073a04e7c6ec730587c'),
(172, 'b2e9686da65e43a7bba2450b208c3a12', '3d6c60947bfa44bab790d1fa35b8b92b'),
(175, 'b2e9686da65e43a7bba2450b208c3a12', 'c359439deb0d4ae9a410fdcf40a0b27a'),
(187, 'b5ecdfdd51f645589b7a53963e90655f', '3d6c60947bfa44bab790d1fa35b8b92b'),
(248, 'beaf07ebd2594e9997724bbcf3609d4b', 'b5241a758bbd4033ac188cb19dfcf438'),
(131, 'c0a77febed5a4416b7b4c822f1121d8e', '0ae8ee156ceb4d6a88896248c137dc7a'),
(132, 'c0a77febed5a4416b7b4c822f1121d8e', '62af5fbeb8bc4bc6a9e367e2ec65b943'),
(133, 'c0a77febed5a4416b7b4c822f1121d8e', '95ed54416acb4e7fa4dd5d50ee1c77d0'),
(241, 'c897be2190ee4e30b40f9ca42fda908f', '21ec1132c8954073a04e7c6ec730587c'),
(217, 'd07061a20bc048d980f30fe107ae2d86', '3227229e245f4022bb4d97644bb5755a'),
(215, 'e242d081296344ee8236925557a53439', '4bcf75ed7c514f829af369a0b517a42f'),
(276, 'e242d081296344ee8236925557a53439', '69c8b06ff95d4e8bb2e7db8f5117cfda'),
(271, 'eac9ac0253564743b6a695fc1af487df', '1f086e154be447cbacb8d682e5117527'),
(157, 'eac9ac0253564743b6a695fc1af487df', '4bcf75ed7c514f829af369a0b517a42f'),
(270, 'eac9ac0253564743b6a695fc1af487df', '69c8b06ff95d4e8bb2e7db8f5117cfda'),
(156, 'eac9ac0253564743b6a695fc1af487df', '8ef8c9b68a8e4c55b6eba82db6c1332b'),
(272, 'eac9ac0253564743b6a695fc1af487df', '9ebac65a5cc046f8a67274ee04397fec'),
(146, 'eac9ac0253564743b6a695fc1af487df', 'dce7710b06234ff8b8bb310da93c2d04'),
(255, 'f1cbe8baa61a4b4db8dcb8af87c7a9a1', '29deace8cd814482a82c60ea04f6ad6a');

-- --------------------------------------------------------

--
-- Структура таблицы `core_subdirection`
--

CREATE TABLE `core_subdirection` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `parent_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `core_subscription`
--

CREATE TABLE `core_subscription` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `total_lessons` smallint UNSIGNED NOT NULL,
  `carried_lessons` smallint UNSIGNED NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `payment_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `student_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `core_subscription`
--

INSERT INTO `core_subscription` (`created_at`, `updated_at`, `id`, `start_date`, `end_date`, `total_lessons`, `carried_lessons`, `amount`, `status`, `notes`, `direction_id`, `payment_id`, `student_id`) VALUES
('2026-07-07 22:56:43.750809', '2026-07-07 23:23:45.738783', '009cac92d10e4dd19cdc46c0ceda60a8', '2026-07-01', '2026-07-15', 3, 0, 1350.00, 'active', '', '4bcf75ed7c514f829af369a0b517a42f', '744c97c20ef8423d9b940cae7f81a4d2', '6400cbcc622f4ccc9417933f597a97f7'),
('2026-07-07 22:40:03.859151', '2026-07-07 22:54:02.080605', '2ad3a703c37e471e8acd08389e14e623', '2026-07-01', '2026-07-13', 2, 0, 900.00, 'active', '', '69c8b06ff95d4e8bb2e7db8f5117cfda', NULL, 'e242d081296344ee8236925557a53439'),
('2026-07-07 22:58:32.589654', '2026-07-07 22:58:32.589688', '529805dee6e245f4b9554f150566671d', '2026-07-01', '2026-07-31', 2, 0, 900.00, 'active', '', '1f086e154be447cbacb8d682e5117527', 'c6d62378b603441f8c14203847bb70ba', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-07 23:01:03.316537', '2026-07-17 08:16:59.478343', '5c9a787235294076b9d12948b1edec3b', '2026-07-01', '2026-07-14', 2, 0, 1600.00, 'active', '', '9ebac65a5cc046f8a67274ee04397fec', '128888dfbd7c4851940240a7bcb60518', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-17 08:14:24.225219', '2026-07-17 08:19:58.226120', '6e8fea899ac5484eb40f82fa96f1dd94', '2026-07-01', '2026-07-14', 2, 0, 0.00, 'active', '', '9ebac65a5cc046f8a67274ee04397fec', NULL, 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 22:54:16.270201', '2026-07-07 22:54:47.567093', '89e2f3ef904d4acbab83410a4ee7362e', '2026-07-01', '2026-07-15', 3, 0, 1350.00, 'active', '', '4bcf75ed7c514f829af369a0b517a42f', 'cc59a07ed31647e3a58b936f6b8450cb', 'e242d081296344ee8236925557a53439'),
('2026-07-07 23:00:16.123407', '2026-07-17 08:16:59.468921', '96bef82f9fd44fa58c3d555a072ea570', '2026-07-01', '2026-07-13', 2, 0, 900.00, 'active', '', '69c8b06ff95d4e8bb2e7db8f5117cfda', 'dd0cc0a94c4d490592dfadccf8faa3fc', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 22:58:09.113275', '2026-07-07 22:58:09.113298', 'b71942feae48453e9a8b10b8b1bf0286', '2026-07-01', '2026-07-31', 3, 0, 1350.00, 'active', '', '4bcf75ed7c514f829af369a0b517a42f', '6f7b9b4909184fe1b2d2808b0fa65ffc', '31cddb9484894e66aa6beefd98a466cc'),
('2026-07-07 23:00:21.929490', '2026-07-17 08:16:59.463960', 'ce490832ce55405ca7332412545edcf2', '2026-07-01', '2026-07-15', 3, 0, 1350.00, 'active', '', '4bcf75ed7c514f829af369a0b517a42f', '798e18ce71ca4f5b90ebec0ec8f788aa', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 23:00:01.495416', '2026-07-17 08:16:59.473631', 'd28fb46e69a3494d8a7f1e973c6bb58c', '2026-07-01', '2026-07-31', 2, 0, 900.00, 'active', '', '1f086e154be447cbacb8d682e5117527', 'fda14a47e0554d2497a9a61ec6f072b8', 'eac9ac0253564743b6a695fc1af487df'),
('2026-07-07 22:52:44.829900', '2026-07-07 23:23:32.600069', 'dd69f06eab9045bfbee354cb55e6b728', '2026-07-01', '2026-07-15', 2, 0, 900.00, 'active', '', '69c8b06ff95d4e8bb2e7db8f5117cfda', 'd9afc8db823646b887d9f7b013865c82', '6400cbcc622f4ccc9417933f597a97f7'),
('2026-07-07 22:57:39.588287', '2026-07-07 22:59:02.439474', 'dd99bf01cf634d92974b1aa3f095e02e', '2026-07-01', '2026-07-31', 1, 0, 800.00, 'active', '', 'e229ce3d79d648d9a86a4588ae3b83dd', '9eeeb20bfd5844a883362965ac51a1b0', '31cddb9484894e66aa6beefd98a466cc');

-- --------------------------------------------------------

--
-- Структура таблицы `core_teacher`
--

CREATE TABLE `core_teacher` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `hire_date` date DEFAULT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_teacher`
--

INSERT INTO `core_teacher` (`created_at`, `updated_at`, `id`, `name`, `phone`, `email`, `hire_date`, `notes`, `user_id`) VALUES
('2026-07-07 21:11:35.554511', '2026-07-07 21:11:35.554511', '101bdf340d3445999dec2b2f17b6590f', 'Филиппова Кристина Евгеньевна', '89061727947', 'kristina_lafe@mail.ru', '2026-07-08', 'преподаватель творческих направлений+ведет вк страницу', NULL),
('2026-07-07 21:11:35.623980', '2026-07-07 21:11:35.623980', '2cb817a399694365a95ad6e4646ace05', 'Тихонова Анастасия Валерьевна', '79370966380', '', '2026-07-08', 'учитель истории, права и обществознания', NULL),
('2026-07-07 21:11:35.661086', '2026-07-07 21:51:01.577055', '4daeb99d5c194f2c828b09e4f12caeb3', 'Черняева Алина Владимировна', '+79954265173', '', NULL, 'Администратор', NULL),
('2026-07-07 21:11:35.632153', '2026-07-07 21:11:35.632153', '5b737bf335a8435783ee5f673f053b6a', 'Кожевникова Наталья Александровна', '79275280861', '', '2026-07-08', 'Логопед-дефектолог', NULL),
('2026-07-07 21:11:35.652892', '2026-07-07 21:11:35.652892', 'a45275793ead43059a022e28726e661c', 'Оленина Ирина Владимировна', '+7 937 722-18-77', '', '2026-07-08', '', NULL),
('2026-07-07 21:11:35.644237', '2026-07-07 21:11:35.644237', 'c36e730dc4154a319fcb9bed7f71f7c0', 'Давтян Нелли Эдуардовна', '+79195433154', '', '2026-07-08', '', NULL),
('2026-07-07 21:11:35.598050', '2026-07-07 21:11:35.598050', 'd79678e98bfa448c92b4bc4b9161ed07', 'Гелунова Наталья Владимировна', '79608893230', 'skeseniya@bk.ru', '2026-07-08', 'учитель начальных классов и русского языка.', NULL),
('2026-07-07 21:11:35.604109', '2026-07-07 21:11:35.604109', 'df13d46f414c4e42b26ad99d1455780c', 'Мартиросян Лусине Арменовна', '79880098977', '', '2026-07-08', 'учитель английского и французского языка', NULL),
('2026-07-07 21:11:35.653808', '2026-07-07 21:11:35.653808', 'df43d11132f340ef8e23a7f7793a7d8e', 'Чекрыгина Елена Валентиновна', '89053975997', '', '2026-07-08', 'Преподаватель по математике, алгебре, геометрии, физике, нач.классы.', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `core_teacher_directions`
--

CREATE TABLE `core_teacher_directions` (
  `id` bigint NOT NULL,
  `teacher_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `direction_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `core_teacher_directions`
--

INSERT INTO `core_teacher_directions` (`id`, `teacher_id`, `direction_id`) VALUES
(131, '101bdf340d3445999dec2b2f17b6590f', '21ec1132c8954073a04e7c6ec730587c'),
(137, '101bdf340d3445999dec2b2f17b6590f', '4bcf75ed7c514f829af369a0b517a42f'),
(134, '101bdf340d3445999dec2b2f17b6590f', '62af5fbeb8bc4bc6a9e367e2ec65b943'),
(136, '101bdf340d3445999dec2b2f17b6590f', '6b143664f8474029b4427ee98783aa6b'),
(139, '101bdf340d3445999dec2b2f17b6590f', '8ef8c9b68a8e4c55b6eba82db6c1332b'),
(138, '101bdf340d3445999dec2b2f17b6590f', '9ebac65a5cc046f8a67274ee04397fec'),
(132, '101bdf340d3445999dec2b2f17b6590f', 'c53cbd288dec450bb9e219c5567c09f7'),
(133, '101bdf340d3445999dec2b2f17b6590f', 'faf8c1a10bc24bc0bb122f07eb1a032a'),
(145, '2cb817a399694365a95ad6e4646ace05', '45848cc6b2cd4ca2b5f86f72e4492e26'),
(144, '2cb817a399694365a95ad6e4646ace05', 'a3d53d84b752456f9397f16789d763b6'),
(147, '5b737bf335a8435783ee5f673f053b6a', '3227229e245f4022bb4d97644bb5755a'),
(146, '5b737bf335a8435783ee5f673f053b6a', 'ccbbcf64dfa84112861e369023e7c209'),
(150, 'a45275793ead43059a022e28726e661c', '3d6c60947bfa44bab790d1fa35b8b92b'),
(148, 'c36e730dc4154a319fcb9bed7f71f7c0', '0ac197ca71fa4600a6648865d90de501'),
(149, 'c36e730dc4154a319fcb9bed7f71f7c0', '629fc477cabd4bc9a7e19d24535201e1'),
(140, 'd79678e98bfa448c92b4bc4b9161ed07', '57aba4fdf1ed43b786d45a95cef0edd8'),
(142, 'df13d46f414c4e42b26ad99d1455780c', '5b53e33b6175457fb386c91ff5ee3726'),
(141, 'df13d46f414c4e42b26ad99d1455780c', 'ffcb712a49ec43638fdbab9887ac0c56'),
(152, 'df43d11132f340ef8e23a7f7793a7d8e', '57aba4fdf1ed43b786d45a95cef0edd8'),
(151, 'df43d11132f340ef8e23a7f7793a7d8e', '62af5fbeb8bc4bc6a9e367e2ec65b943');

-- --------------------------------------------------------

--
-- Структура таблицы `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-07-01 14:48:29.735007', '2', 'Elena', 1, '[{\"added\": {}}]', 4, 1),
(2, '2026-07-07 21:13:45.212372', '18405078-aab5-4f44-915c-6e2528326202', 'Соня', 3, '', 20, 1),
(3, '2026-07-07 21:13:45.212372', '2c36915d-daae-44a2-af13-98c7cc6a5527', 'София', 3, '', 20, 1),
(4, '2026-07-07 21:18:18.661971', '99592f4f-2ebe-438f-8116-5459f95797bb', '\"Скоро в школу\" (5-6 лет) (Милана)', 3, '', 11, 1),
(5, '2026-07-07 21:18:18.661971', 'd4357905-a7a4-4dbf-b74f-d2f676628259', 'Вокальная студия \"Творческий пульс\" с 9 лет (Соня)', 3, '', 11, 1),
(6, '2026-07-07 21:18:18.661971', 'f9fd39da-0d84-492a-8a7e-4b0dd9211b55', 'Занимательный английский', 3, '', 11, 1),
(7, '2026-07-07 21:18:18.661971', '6dbd026d-8ae8-45d3-ac93-5581c2182ac0', 'индивидуальное занятие по математике (Катя)', 3, '', 11, 1),
(8, '2026-07-07 21:18:18.661971', '2c6d9817-61dc-4adf-b5d1-a4b9aad48d57', 'Индивидуальное занятие по математике и русскому языку  (Ермаков)', 3, '', 11, 1),
(9, '2026-07-07 21:18:18.661971', '7a364159-a9ab-4bd5-840d-4b9b3b0822f9', 'Индивидуальное занятие по математике и русскому языку (2 класс)', 3, '', 11, 1),
(10, '2026-07-07 21:18:18.661971', 'ec1f472b-c417-4f07-8e6b-ddf658951c28', 'Индивидуальное занятие по математике и русскому языку (2 класс) (Костя )', 3, '', 11, 1),
(11, '2026-07-07 21:18:18.661971', '651aabe7-9517-43d6-95f2-679ce28f20ac', 'Индивидуальное занятие по математике и русскому языку (2 класс) (Костя)', 3, '', 11, 1),
(12, '2026-07-07 21:18:18.661971', '73c3a5b6-d395-4b1f-afc7-681eede5e687', 'Индивидуальное занятие по математике и русскому языку (2 класс) (Марфа)', 3, '', 11, 1),
(13, '2026-07-07 21:18:18.661971', '2f3ed60f-8b07-4988-9974-2f54cfb5b03c', 'Индивидуальные занятия по алгебре (Есения)', 3, '', 11, 1),
(14, '2026-07-07 21:18:18.661971', '03ddf301-2b82-44f2-a531-85fc5ef55c61', 'Индивидуальные занятия по английскому (Вика)', 3, '', 11, 1),
(15, '2026-07-07 21:18:18.661971', '291661d4-b5bb-4afa-bc96-44d5236c603e', 'Индивидуальные занятия по английскому языку (4 класс)', 3, '', 11, 1),
(16, '2026-07-07 21:18:18.661971', 'c31d8920-49d2-4191-8b51-0eb0224151fd', 'Индивидуальные занятия по английскому языку (Аверина Юлия )', 3, '', 11, 1),
(17, '2026-07-07 21:18:18.661971', 'aa116ac5-2ce5-4839-ad43-9347e882bfa6', 'Индивидуальные занятия по английскому языку (Анфиса)', 3, '', 11, 1),
(18, '2026-07-07 21:18:18.661971', 'cd59b338-0dd8-4d93-978e-caa4752efbad', 'Индивидуальные занятия по английскому языку (Арен)', 3, '', 11, 1),
(19, '2026-07-07 21:18:18.661971', '3a10dde6-145f-41b4-aa82-8cce16257170', 'Индивидуальные занятия по английскому языку (Артем Панфилов), 4  класс)', 3, '', 11, 1),
(20, '2026-07-07 21:18:18.661971', '1fc5c6fd-a916-4ed1-acf7-07010dff9b13', 'Индивидуальные занятия по английскому языку (Артём)', 3, '', 11, 1),
(21, '2026-07-07 21:18:18.661971', 'a9d95a61-0ce4-4ba0-9dd1-05077e89257e', 'Индивидуальные занятия по английскому языку (Вова)', 3, '', 11, 1),
(22, '2026-07-07 21:18:18.661971', '4fa0f6a5-5a52-4749-bcbf-41f51a415f69', 'Индивидуальные занятия по английскому языку (Давид)', 3, '', 11, 1),
(23, '2026-07-07 21:18:18.661971', '1fa8d42a-82bd-4c06-b204-b8e0d363aa76', 'Индивидуальные занятия по английскому языку (Дарина)', 3, '', 11, 1),
(24, '2026-07-07 21:18:18.661971', 'af74935e-5251-481a-91e2-5385fd1583bf', 'Индивидуальные занятия по английскому языку (Ева)', 3, '', 11, 1),
(25, '2026-07-07 21:18:18.661971', '4acd3ddc-60ac-49d7-965a-49a3de2ebe2c', 'Индивидуальные занятия по английскому языку (Ермаков)', 3, '', 11, 1),
(26, '2026-07-07 21:18:18.661971', 'a9262298-7942-45ce-a66d-83c5b1ac081d', 'Индивидуальные занятия по английскому языку (Ермилова София)', 3, '', 11, 1),
(27, '2026-07-07 21:18:18.661971', 'a139ad66-d7a4-4391-9d5e-94c827712101', 'Индивидуальные занятия по английскому языку (Ковалев Алексей)', 3, '', 11, 1),
(28, '2026-07-07 21:18:18.661971', '9f6d2a5b-10e1-4bd1-b3ad-63bc4dc90615', 'Индивидуальные занятия по английскому языку (Марьяна)', 3, '', 11, 1),
(29, '2026-07-07 21:18:18.661971', '9c9b84de-70a4-4c94-b7d8-59a23527522b', 'Индивидуальные занятия по английскому языку (Матвей)', 3, '', 11, 1),
(30, '2026-07-07 21:18:18.661971', '913fc746-00d0-4192-b37e-f3a3472ef5bf', 'Индивидуальные занятия по английскому языку (Маша)', 3, '', 11, 1),
(31, '2026-07-07 21:18:18.661971', '6d890828-f8a9-4249-8f73-9547baa0fd32', 'Индивидуальные занятия по английскому языку (Милана)', 3, '', 11, 1),
(32, '2026-07-07 21:18:18.661971', 'c5752bbc-e204-4831-af22-ac73cf088a2e', 'Индивидуальные занятия по английскому языку (Никита)', 3, '', 11, 1),
(33, '2026-07-07 21:18:18.661971', '77964820-8269-49ea-a4c0-6bf8a24665d8', 'Индивидуальные занятия по гитаре (Алиса)', 3, '', 11, 1),
(34, '2026-07-07 21:18:18.661971', '50897720-1065-4a7c-ace9-c63a9d5a5463', 'Индивидуальные занятия по гитаре (Есения)', 3, '', 11, 1),
(35, '2026-07-07 21:18:18.661971', '4228433a-48c1-40f8-bf10-d85ab902de51', 'Индивидуальные занятия по гитаре (Надя)', 3, '', 11, 1),
(36, '2026-07-07 21:18:18.661971', 'c6e2aaf2-bf99-4fa8-b8ba-7818c071fb68', 'Индивидуальные занятия по гитаре (Софа)', 3, '', 11, 1),
(37, '2026-07-07 21:18:18.661971', '6bb2ea9a-5154-4d2d-a4a7-792eeb19bc87', 'Индивидуальные занятия по гитаре (Ярослав)', 3, '', 11, 1),
(38, '2026-07-07 21:18:18.661971', '16dc55a6-dea0-4a94-90f5-c95e1e97618d', 'Индивидуальные занятия по математике (Анфиса)', 3, '', 11, 1),
(39, '2026-07-07 21:18:18.661971', '9d5eeda9-21b3-4510-b30f-572c74b7da0d', 'Индивидуальные занятия по математике (Ваня)', 3, '', 11, 1),
(40, '2026-07-07 21:18:18.661971', 'a0b2ca25-17c3-4161-bb20-8a8fae5f6d45', 'Индивидуальные занятия по математике (Вероника)', 3, '', 11, 1),
(41, '2026-07-07 21:18:18.661971', '76507b63-bab4-43d5-af4f-22804aa9fcf5', 'Индивидуальные занятия по математике (Давид)', 3, '', 11, 1),
(42, '2026-07-07 21:18:18.661971', 'c6e63c17-36b4-428a-b60e-54429901e79d', 'Индивидуальные занятия по математике (Дима)', 3, '', 11, 1),
(43, '2026-07-07 21:18:18.661971', '6820c599-ca8a-4f52-a843-84dc032e8cf8', 'Индивидуальные занятия по математике (Илья)', 3, '', 11, 1),
(44, '2026-07-07 21:18:18.661971', '5c7242a3-12c8-4110-b305-5b8a73eb22a8', 'Индивидуальные занятия по математике (Костя 8 класс)', 3, '', 11, 1),
(45, '2026-07-07 21:18:18.661971', 'e3046eea-e30d-4a47-9dfd-7d4ef999dd1f', 'Индивидуальные занятия по математике (Мария)', 3, '', 11, 1),
(46, '2026-07-07 21:18:18.661971', 'c30fbb23-f61c-4588-903c-8b8644574f6e', 'Индивидуальные занятия по математике (Полина)', 3, '', 11, 1),
(47, '2026-07-07 21:18:18.661971', 'ae6bc1a6-1922-4db9-b1d4-2f2f4c2f2437', 'Индивидуальные занятия по математике (Соня)', 3, '', 11, 1),
(48, '2026-07-07 21:18:18.661971', '5cfa00c3-643d-4b7e-97e0-917848e7c66e', 'Индивидуальные занятия по русскому языку (Анфиса)', 3, '', 11, 1),
(49, '2026-07-07 21:18:18.661971', '6eeeeea5-dd90-439e-8f61-ac00916f92db', 'Индивидуальные занятия по русскому языку (Ваня)', 3, '', 11, 1),
(50, '2026-07-07 21:18:18.661971', 'e98f482d-c981-412b-877e-e71969201f72', 'Индивидуальные занятия по русскому языку (Дима)', 3, '', 11, 1),
(51, '2026-07-07 21:18:18.661971', '7bbd33b8-d6f5-4823-b1db-73d64722a38b', 'Индивидуальные занятия по русскому языку (Катя)', 3, '', 11, 1),
(52, '2026-07-07 21:18:18.661971', '195dbd73-48c0-4492-9c19-cf63cbe3f4c0', 'Индивидуальные занятия по русскому языку (Костя)', 3, '', 11, 1),
(53, '2026-07-07 21:18:18.661971', 'b341223c-e4b7-4129-880c-f5811f6ddff7', 'Индивидуальные занятия по русскому языку (Соня)', 3, '', 11, 1),
(54, '2026-07-07 21:18:18.661971', 'da0913a7-34aa-46cb-92c5-c02687dd49b4', 'Индивидуальные занятия по физике (Есения)', 3, '', 11, 1),
(55, '2026-07-07 21:18:18.661971', 'eab49e23-3e24-43c2-9254-875719c08122', 'Индивидуальные занятия по чтению (Аня Потапова)', 3, '', 11, 1),
(56, '2026-07-07 21:18:18.661971', 'b724fbbe-316a-496d-ac60-cccb49a325eb', 'Индивидуальные занятия по чтению (Василиса )', 3, '', 11, 1),
(57, '2026-07-07 21:18:18.661971', '86934e8b-655c-4970-be81-98d8577e0458', 'Курс \"Пишу красиво\" (1-4 класс) индивидуально (Вика)', 3, '', 11, 1),
(58, '2026-07-07 21:18:18.661971', 'a9de753e-45a0-49bf-b92c-14b29c5f977c', 'Курс \"Пишу красиво\" (1-4 класс) индивидуально (Егор)', 3, '', 11, 1),
(59, '2026-07-07 21:18:18.661971', '1f9177df-7c5c-4ffd-9dab-1251c853207e', 'Логопедические занятия (Аня Ключникова)', 3, '', 11, 1),
(60, '2026-07-07 21:18:18.661971', 'eb3ba0e6-bda5-435f-a4a5-d52991cc785b', 'Логопедические занятия (Аня)', 3, '', 11, 1),
(61, '2026-07-07 21:18:18.661971', 'be816805-8b64-4a13-bf7c-6be2bef1280a', 'Логопедические занятия (Дегтянникова Амелия)', 3, '', 11, 1),
(62, '2026-07-07 21:18:18.661971', 'bc0a959d-2909-44f0-8f7e-03dfd18a747a', 'Танцевальная студия \"Бусинки\" с 3 лет', 3, '', 11, 1),
(63, '2026-07-07 21:18:18.661971', 'c657e4b3-1abc-4ff5-bb13-b2ee4dc1ad72', 'Танцевальная студия \"Грация\" с 7 лет (Есения)', 3, '', 11, 1),
(64, '2026-07-07 21:18:18.661971', '9f779784-47f6-4b93-81ae-d5a5a1731d5f', 'танцевальная студия \"Забава\"', 3, '', 11, 1),
(65, '2026-07-07 21:18:18.661971', '129c2fa5-e03f-45cb-8e00-9768c15212b1', 'Театральная студия с 5 лет', 3, '', 11, 1),
(66, '2026-07-07 21:27:56.490872', '3', 'Nataliya-director', 1, '[{\"added\": {}}]', 4, 1),
(67, '2026-07-07 21:31:39.085578', '3', 'Nataliya-director — Директор', 2, '[{\"changed\": {\"fields\": [\"\\u0420\\u043e\\u043b\\u044c \\u0432 CRM\"]}}]', 25, 1),
(68, '2026-07-07 21:32:17.756997', '2', 'Elena', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 1),
(69, '2026-07-07 21:32:25.784253', '2', 'Elena — Ресепшн', 2, '[]', 25, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(25, 'accounts', 'userprofile'),
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'core', 'attendancerecord'),
(8, 'core', 'auditlog'),
(9, 'core', 'centersettings'),
(10, 'core', 'classroom'),
(11, 'core', 'direction'),
(12, 'core', 'kanbantask'),
(13, 'core', 'materialpurchase'),
(14, 'core', 'newsitem'),
(15, 'core', 'parent'),
(16, 'core', 'payment'),
(17, 'core', 'scheduleexception'),
(18, 'core', 'scheduleslot'),
(19, 'core', 'singlelesson'),
(20, 'core', 'student'),
(21, 'core', 'subdirection'),
(22, 'core', 'subscription'),
(23, 'core', 'teacher'),
(24, 'core', 'teacherpayrollperiod'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Структура таблицы `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-06-18 06:14:20.679884'),
(2, 'auth', '0001_initial', '2026-06-18 06:14:21.731675'),
(3, 'admin', '0001_initial', '2026-06-18 06:14:21.941700'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-06-18 06:14:21.953057'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-06-18 06:14:21.962047'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-06-18 06:14:22.103024'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-06-18 06:14:22.201769'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-06-18 06:14:22.260535'),
(9, 'auth', '0004_alter_user_username_opts', '2026-06-18 06:14:22.269532'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-06-18 06:14:22.367816'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-06-18 06:14:22.370740'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-06-18 06:14:22.378741'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-06-18 06:14:22.488065'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-06-18 06:14:22.595400'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-06-18 06:14:22.646544'),
(16, 'auth', '0011_update_proxy_permissions', '2026-06-18 06:14:22.655539'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-06-18 06:14:22.773110'),
(18, 'core', '0001_initial', '2026-06-18 06:14:26.949660'),
(19, 'sessions', '0001_initial', '2026-06-18 06:14:27.015553'),
(20, 'core', '0002_direction_lesson_type_and_prices', '2026-06-18 14:14:54.938719'),
(21, 'core', '0003_scheduleslot_sort_order', '2026-06-18 15:15:01.324237'),
(22, 'core', '0004_teacher_payroll_and_creative_directions', '2026-07-01 08:15:09.215904'),
(23, 'core', '0005_simplify_teacher_salary', '2026-07-01 08:49:35.162559'),
(24, 'core', '0006_schedule_slot_student', '2026-07-01 09:13:10.622193'),
(25, 'accounts', '0001_initial', '2026-07-01 14:41:27.735658'),
(26, 'accounts', '0002_assign_initial_roles', '2026-07-01 14:42:44.282897');

-- --------------------------------------------------------

--
-- Структура таблицы `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1jy6uk8leqybulu9j3n2jxxsl5v1pvwr', '.eJxVjEEOwiAQAP_C2ZAuZQU8eu8bmi3sStVAUtqT8e_apAe9zkzmpUba1jxujZdxTuqiQJ1-2UTxwWUX6U7lVnWsZV3mSe-JPmzTQ038vB7t3yBTy_v2HKwBYRDsbEQDzvXeCYsJ4n20Aj2Y4JGRpq8lpI47NNwLBh8I1fsDu4Q28Q:1waEVf:cnVlXp97WkIO8urCnTaeNh1OHH6DrCqA6-ow-pr1gTk', '2026-07-02 15:18:27.836393'),
('1ta70bl7npejcd3rk6a9xu3evf2r7dbs', '.eJxVjDsOwjAQBe_iGlleWH-Wkp4zRPaugwPIluKkQtwdIqWA9s3Me6khrksZ1p7nYRJ1VqAOv1uK_Mh1A3KP9dY0t7rMU9Kbonfa9bVJfl529--gxF6-NVkXiNmbEDJkBx4TGHB0QhHPiQUtIY6AkJCO7NFEZoiCNFpyQOr9AcL0NyQ:1whRFq:09kPo_lddCc0eLUXpfc9KDnxBLRSMYLMeMsdBHfOQcY', '2026-07-22 12:19:54.331199'),
('25enqly2wjosmu9ksffwo1cn2jlvjqv7', '.eJxVjDsOwjAQBe_iGll448ReSvqcwXq2NySAbCmfCnF3iJQC2jcz76UCtnUM2yJzmLK6KKNOv1tEekjZQb6j3KpOtazzFPWu6IMuuq9ZntfD_TsYsYzfmnCGcOsdW48c2afOomNqXRpsQ4MT01ELOBDIk42mQSNePCOBrVPvD9lxN7A:1whD1t:nZKNDsmtoqQYWENN489ACG1X_k59IlP75gvT4IoS-go', '2026-07-21 21:08:33.125751'),
('8i9zeld5n1ofiq05liscat5pnf0hc3pu', '.eJxVjE0OwiAYBe_C2hB-SgGX7j0DefCBVA1NSrsy3l2bdKHbNzPvxQK2tYat5yVMxM5MsdPvFpEeue2A7mi3mae5rcsU-a7wg3Z-nSk_L4f7d1DR67d2UZMX8LAjbIoeMEAqpFH0QE5giFoYaYywQjqlpFHFFUmx2DSiZPb-AP10OHw:1whDQQ:p5o9TqLNxXfkvxHPdebIB6csrGClQG9xUp_PmXflr9M', '2026-07-21 21:33:54.920708'),
('dqggk0ixacd0fzhreylotgwuzd1myyn7', '.eJxVjEEOwiAQAP_C2ZAuZQU8eu8bmi3sStVAUtqT8e_apAe9zkzmpUba1jxujZdxTuqiQJ1-2UTxwWUX6U7lVnWsZV3mSe-JPmzTQ038vB7t3yBTy_v2HKwBYRDsbEQDzvXeCYsJ4n20Aj2Y4JGRpq8lpI47NNwLBh8I1fsDu4Q28Q:1wa62p:E2umLfbPl2lSomr1U-Kg-fjv8dAneECLGMsXOTWGf34', '2026-07-02 06:16:07.829348'),
('en6rsso96x7h5l5gd97l2vtrt4myxm7z', '.eJxVjDsOwjAQBe_iGlleWH-Wkp4zRPaugwPIluKkQtwdIqWA9s3Me6khrksZ1p7nYRJ1VqAOv1uK_Mh1A3KP9dY0t7rMU9Kbonfa9bVJfl529--gxF6-NVkXiNmbEDJkBx4TGHB0QhHPiQUtIY6AkJCO7NFEZoiCNFpyQOr9AcL0NyQ:1wkdQ3:2v34ncqPvmrRysGfLUcVWq6KKlpRvlMT9lg9RLzMiUA', '2026-07-31 07:55:39.084497'),
('f6hqck8mhjpv9rv57sp9l9owddl7sgcv', '.eJxVjDsOwjAQBe_iGll448ReSvqcwXq2NySAbCmfCnF3iJQC2jcz76UCtnUM2yJzmLK6KKNOv1tEekjZQb6j3KpOtazzFPWu6IMuuq9ZntfD_TsYsYzfmnCGcOsdW48c2afOomNqXRpsQ4MT01ELOBDIk42mQSNePCOBrVPvD9lxN7A:1whD1N:w3nSSy3FkF3wJrCuLpCqm7GWCRRJdkvdJT1kHy6k3EM', '2026-07-21 21:08:01.891492'),
('nezmz6dsgytu61ssiu4gglp7di86j9yy', '.eJxVjDsOwjAQBe_iGlleWH-Wkp4zRPaugwPIluKkQtwdIqWA9s3Me6khrksZ1p7nYRJ1VqAOv1uK_Mh1A3KP9dY0t7rMU9Kbonfa9bVJfl529--gxF6-NVkXiNmbEDJkBx4TGHB0QhHPiQUtIY6AkJCO7NFEZoiCNFpyQOr9AcL0NyQ:1whnUS:xTU9yg4ciYl84gqCQPIR2AbNBDV86MnJBQ7UNl7KaFg', '2026-07-23 12:04:28.774651'),
('phl2d2e64hunccl0kn4lav04g401xcqs', '.eJxVjE0OwiAYBe_C2hB-SgGX7j0DefCBVA1NSrsy3l2bdKHbNzPvxQK2tYat5yVMxM5MsdPvFpEeue2A7mi3mae5rcsU-a7wg3Z-nSk_L4f7d1DR67d2UZMX8LAjbIoeMEAqpFH0QE5giFoYaYywQjqlpFHFFUmx2DSiZPb-AP10OHw:1wkdZU:3A9tLbgLyAj1g7VkuIyAbcqjUufw9hJf-A56cU8e4RU', '2026-07-31 08:05:24.126999'),
('qm5wxf4gdrnpv28tv789lafom00hxwqo', '.eJxVjEEOwiAQAP_C2ZAuZQU8eu8bmi3sStVAUtqT8e_apAe9zkzmpUba1jxujZdxTuqiQJ1-2UTxwWUX6U7lVnWsZV3mSe-JPmzTQ038vB7t3yBTy_v2HKwBYRDsbEQDzvXeCYsJ4n20Aj2Y4JGRpq8lpI47NNwLBh8I1fsDu4Q28Q:1werDO:eLZoJf1KAGW-JnMmALlgSHT8w7dzHiRoMQVwi2UomRc', '2026-07-15 09:26:42.993208'),
('zz4kejb27l631iw2w2cx8t2ataulm8yy', '.eJxVjEEOwiAQAP_C2ZAuZQU8eu8bmi3sStVAUtqT8e_apAe9zkzmpUba1jxujZdxTuqiQJ1-2UTxwWUX6U7lVnWsZV3mSe-JPmzTQ038vB7t3yBTy_v2HKwBYRDsbEQDzvXeCYsJ4n20Aj2Y4JGRpq8lpI47NNwLBh8I1fsDu4Q28Q:1wewHJ:tHtcgsfSGUzQkx1UZG3izX4tDhDKBz0nSXBh8EjXv4w', '2026-07-15 14:51:05.360729');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `accounts_userprofile`
--
ALTER TABLE `accounts_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Индексы таблицы `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Индексы таблицы `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Индексы таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Индексы таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `core_attendancerecord`
--
ALTER TABLE `core_attendancerecord`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_attendancerecord_direction_id_69d38498_fk_core_direction_id` (`direction_id`),
  ADD KEY `core_attendancerecor_schedule_slot_id_62899434_fk_core_sche` (`schedule_slot_id`),
  ADD KEY `core_attendancerecor_single_lesson_id_f747c905_fk_core_sing` (`single_lesson_id`),
  ADD KEY `core_attendancerecord_student_id_601f7971_fk_core_student_id` (`student_id`),
  ADD KEY `core_attendancerecor_subscription_id_a2609dfc_fk_core_subs` (`subscription_id`);

--
-- Индексы таблицы `core_auditlog`
--
ALTER TABLE `core_auditlog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_auditlog_user_id_3797aaab_fk_auth_user_id` (`user_id`);

--
-- Индексы таблицы `core_centersettings`
--
ALTER TABLE `core_centersettings`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `core_classroom`
--
ALTER TABLE `core_classroom`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `core_direction`
--
ALTER TABLE `core_direction`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `core_kanbantask`
--
ALTER TABLE `core_kanbantask`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_kanbantask_assignee_id_b83a5350_fk_auth_user_id` (`assignee_id`);

--
-- Индексы таблицы `core_materialpurchase`
--
ALTER TABLE `core_materialpurchase`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_materialpurchase_direction_id_cad01443_fk_core_direction_id` (`direction_id`);

--
-- Индексы таблицы `core_newsitem`
--
ALTER TABLE `core_newsitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_newsitem_author_id_e0aafcb5_fk_auth_user_id` (`author_id`);

--
-- Индексы таблицы `core_parent`
--
ALTER TABLE `core_parent`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `core_payment`
--
ALTER TABLE `core_payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_payment_created_by_id_5835508b_fk_auth_user_id` (`created_by_id`),
  ADD KEY `core_payment_direction_id_36a89aa1_fk_core_direction_id` (`direction_id`),
  ADD KEY `core_payment_student_id_96571bb6_fk_core_student_id` (`student_id`);

--
-- Индексы таблицы `core_scheduleexception`
--
ALTER TABLE `core_scheduleexception`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_scheduleexception_lesson_date_schedule_slo_2c4af034_uniq` (`lesson_date`,`schedule_slot_id`),
  ADD KEY `core_scheduleexcepti_schedule_slot_id_6de28c36_fk_core_sche` (`schedule_slot_id`),
  ADD KEY `core_scheduleexcepti_substitute_teacher_i_ba22581c_fk_core_teac` (`substitute_teacher_id`);

--
-- Индексы таблицы `core_scheduleslot`
--
ALTER TABLE `core_scheduleslot`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_scheduleslot_classroom_id_ddd4b474_fk_core_classroom_id` (`classroom_id`),
  ADD KEY `core_scheduleslot_direction_id_ddb1ee58_fk_core_direction_id` (`direction_id`),
  ADD KEY `core_scheduleslot_subdirection_id_86091b91_fk_core_subd` (`subdirection_id`),
  ADD KEY `core_scheduleslot_teacher_id_ec7e053d_fk_core_teacher_id` (`teacher_id`),
  ADD KEY `core_scheduleslot_student_id_5f448ba3_fk_core_student_id` (`student_id`);

--
-- Индексы таблицы `core_singlelesson`
--
ALTER TABLE `core_singlelesson`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_singlelesson_classroom_id_13269fa4_fk_core_classroom_id` (`classroom_id`),
  ADD KEY `core_singlelesson_created_by_id_51f6ec86_fk_auth_user_id` (`created_by_id`),
  ADD KEY `core_singlelesson_direction_id_8974c351_fk_core_direction_id` (`direction_id`),
  ADD KEY `core_singlelesson_student_id_5a9c4f51_fk_core_student_id` (`student_id`),
  ADD KEY `core_singlelesson_teacher_id_3dc4641f_fk_core_teacher_id` (`teacher_id`);

--
-- Индексы таблицы `core_student`
--
ALTER TABLE `core_student`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_student_parent_id_60157d65_fk_core_parent_id` (`parent_id`);

--
-- Индексы таблицы `core_student_directions`
--
ALTER TABLE `core_student_directions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_student_directions_student_id_direction_id_02a4a70f_uniq` (`student_id`,`direction_id`),
  ADD KEY `core_student_directi_direction_id_581b82e3_fk_core_dire` (`direction_id`);

--
-- Индексы таблицы `core_subdirection`
--
ALTER TABLE `core_subdirection`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_subdirection_parent_id_name_342007be_uniq` (`parent_id`,`name`);

--
-- Индексы таблицы `core_subscription`
--
ALTER TABLE `core_subscription`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `payment_id` (`payment_id`),
  ADD KEY `core_subscription_direction_id_c306f633_fk_core_direction_id` (`direction_id`),
  ADD KEY `core_subscription_student_id_b57ede4e_fk_core_student_id` (`student_id`);

--
-- Индексы таблицы `core_teacher`
--
ALTER TABLE `core_teacher`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Индексы таблицы `core_teacher_directions`
--
ALTER TABLE `core_teacher_directions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_teacher_directions_teacher_id_direction_id_102ff6a3_uniq` (`teacher_id`,`direction_id`),
  ADD KEY `core_teacher_directi_direction_id_38eb93d7_fk_core_dire` (`direction_id`);

--
-- Индексы таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Индексы таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Индексы таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `accounts_userprofile`
--
ALTER TABLE `accounts_userprofile`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT для таблицы `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `core_auditlog`
--
ALTER TABLE `core_auditlog`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT для таблицы `core_centersettings`
--
ALTER TABLE `core_centersettings`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `core_student_directions`
--
ALTER TABLE `core_student_directions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=277;

--
-- AUTO_INCREMENT для таблицы `core_teacher_directions`
--
ALTER TABLE `core_teacher_directions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=155;

--
-- AUTO_INCREMENT для таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT для таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT для таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `accounts_userprofile`
--
ALTER TABLE `accounts_userprofile`
  ADD CONSTRAINT `accounts_userprofile_user_id_92240672_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_attendancerecord`
--
ALTER TABLE `core_attendancerecord`
  ADD CONSTRAINT `core_attendancerecor_schedule_slot_id_62899434_fk_core_sche` FOREIGN KEY (`schedule_slot_id`) REFERENCES `core_scheduleslot` (`id`),
  ADD CONSTRAINT `core_attendancerecor_single_lesson_id_f747c905_fk_core_sing` FOREIGN KEY (`single_lesson_id`) REFERENCES `core_singlelesson` (`id`),
  ADD CONSTRAINT `core_attendancerecor_subscription_id_a2609dfc_fk_core_subs` FOREIGN KEY (`subscription_id`) REFERENCES `core_subscription` (`id`),
  ADD CONSTRAINT `core_attendancerecord_direction_id_69d38498_fk_core_direction_id` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`),
  ADD CONSTRAINT `core_attendancerecord_student_id_601f7971_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_auditlog`
--
ALTER TABLE `core_auditlog`
  ADD CONSTRAINT `core_auditlog_user_id_3797aaab_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_kanbantask`
--
ALTER TABLE `core_kanbantask`
  ADD CONSTRAINT `core_kanbantask_assignee_id_b83a5350_fk_auth_user_id` FOREIGN KEY (`assignee_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_materialpurchase`
--
ALTER TABLE `core_materialpurchase`
  ADD CONSTRAINT `core_materialpurchase_direction_id_cad01443_fk_core_direction_id` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_newsitem`
--
ALTER TABLE `core_newsitem`
  ADD CONSTRAINT `core_newsitem_author_id_e0aafcb5_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_payment`
--
ALTER TABLE `core_payment`
  ADD CONSTRAINT `core_payment_created_by_id_5835508b_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_payment_direction_id_36a89aa1_fk_core_direction_id` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`),
  ADD CONSTRAINT `core_payment_student_id_96571bb6_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_scheduleexception`
--
ALTER TABLE `core_scheduleexception`
  ADD CONSTRAINT `core_scheduleexcepti_schedule_slot_id_6de28c36_fk_core_sche` FOREIGN KEY (`schedule_slot_id`) REFERENCES `core_scheduleslot` (`id`),
  ADD CONSTRAINT `core_scheduleexcepti_substitute_teacher_i_ba22581c_fk_core_teac` FOREIGN KEY (`substitute_teacher_id`) REFERENCES `core_teacher` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_scheduleslot`
--
ALTER TABLE `core_scheduleslot`
  ADD CONSTRAINT `core_scheduleslot_classroom_id_ddd4b474_fk_core_classroom_id` FOREIGN KEY (`classroom_id`) REFERENCES `core_classroom` (`id`),
  ADD CONSTRAINT `core_scheduleslot_direction_id_ddb1ee58_fk_core_direction_id` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`),
  ADD CONSTRAINT `core_scheduleslot_student_id_5f448ba3_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`),
  ADD CONSTRAINT `core_scheduleslot_subdirection_id_86091b91_fk_core_subd` FOREIGN KEY (`subdirection_id`) REFERENCES `core_subdirection` (`id`),
  ADD CONSTRAINT `core_scheduleslot_teacher_id_ec7e053d_fk_core_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_singlelesson`
--
ALTER TABLE `core_singlelesson`
  ADD CONSTRAINT `core_singlelesson_classroom_id_13269fa4_fk_core_classroom_id` FOREIGN KEY (`classroom_id`) REFERENCES `core_classroom` (`id`),
  ADD CONSTRAINT `core_singlelesson_created_by_id_51f6ec86_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_singlelesson_direction_id_8974c351_fk_core_direction_id` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`),
  ADD CONSTRAINT `core_singlelesson_student_id_5a9c4f51_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`),
  ADD CONSTRAINT `core_singlelesson_teacher_id_3dc4641f_fk_core_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_student`
--
ALTER TABLE `core_student`
  ADD CONSTRAINT `core_student_parent_id_60157d65_fk_core_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `core_parent` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_student_directions`
--
ALTER TABLE `core_student_directions`
  ADD CONSTRAINT `core_student_directi_direction_id_581b82e3_fk_core_dire` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`),
  ADD CONSTRAINT `core_student_directions_student_id_f8d8855d_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_subdirection`
--
ALTER TABLE `core_subdirection`
  ADD CONSTRAINT `core_subdirection_parent_id_1d1c704b_fk_core_direction_id` FOREIGN KEY (`parent_id`) REFERENCES `core_direction` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_subscription`
--
ALTER TABLE `core_subscription`
  ADD CONSTRAINT `core_subscription_direction_id_c306f633_fk_core_direction_id` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`),
  ADD CONSTRAINT `core_subscription_payment_id_fd58b1ec_fk_core_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `core_payment` (`id`),
  ADD CONSTRAINT `core_subscription_student_id_b57ede4e_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_teacher`
--
ALTER TABLE `core_teacher`
  ADD CONSTRAINT `core_teacher_user_id_0d56ab99_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `core_teacher_directions`
--
ALTER TABLE `core_teacher_directions`
  ADD CONSTRAINT `core_teacher_directi_direction_id_38eb93d7_fk_core_dire` FOREIGN KEY (`direction_id`) REFERENCES `core_direction` (`id`),
  ADD CONSTRAINT `core_teacher_directions_teacher_id_026d430b_fk_core_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`id`);

--
-- Ограничения внешнего ключа таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
