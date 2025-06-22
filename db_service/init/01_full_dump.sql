-- CREATE USER dotnetdon_admin WITH PASSWORD '4MTGbthhIFpQS4V';
-- CREATE DATABASE vpndotnetdotv2 OWNER dotnetdon_admin;

-- -- даём базовые привилегии
GRANT ALL PRIVILEGES ON DATABASE vpndotnetdotv2 TO dotnetdon_admin;

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Key; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Key" (
    id integer NOT NULL,
    user_id integer NOT NULL,
    key_content character varying,
    active_until date NOT NULL,
    order_id integer NOT NULL,
    key_id character varying
);


ALTER TABLE public."Key" OWNER TO postgres;

--
-- Name: Key_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Key" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Key_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: Order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Order" (
    id integer NOT NULL,
    order_price integer NOT NULL,
    create_date date NOT NULL,
    is_paid boolean NOT NULL,
    user_id integer NOT NULL,
    platform character varying NOT NULL
);


ALTER TABLE public."Order" OWNER TO postgres;

--
-- Name: Order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Order" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Order_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    id integer NOT NULL,
    tg_id bigint NOT NULL,
    test_used boolean DEFAULT false NOT NULL,
    tg_username character varying(100),
    is_premium boolean DEFAULT false NOT NULL,
    email character varying
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."User" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."User_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: Key; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Key" (id, user_id, key_content, active_until, order_id, key_id) FROM stdin;
34	15	http://88.218.169.237:22045/subDKJVT35/cec664_sauvingnon	2025-05-17	75	57f0cfde-6990-4738-a5f7-dc7dd9806dd2
\.


--
-- Data for Name: Order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Order" (id, order_price, create_date, is_paid, user_id, platform) FROM stdin;
75	80	2025-04-17	f	15	platform_ios
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."User" (id, tg_id, test_used, tg_username, is_premium, email) FROM stdin;
14	5609041446	f	\N	t	\N
15	542049460	f	sauvingnon	t	\N
19	917179154	f	Geckonda	t	\N
34	1023042057	f	kirekara	t	\N
35	1575950879	f	kamel_lka	t	\N
\.


--
-- Name: Key_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Key_id_seq"', 34, true);


--
-- Name: Order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Order_id_seq"', 75, true);


--
-- Name: User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."User_id_seq"', 45, true);


--
-- Name: Key Key_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Key"
    ADD CONSTRAINT "Key_pkey" PRIMARY KEY (id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: Order id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Order"
    ADD CONSTRAINT id PRIMARY KEY (id);


--
-- Name: Key order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Key"
    ADD CONSTRAINT order_id FOREIGN KEY (order_id) REFERENCES public."Order"(id) NOT VALID;


--
-- Name: Order user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Order"
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- Name: Key user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Key"
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public."User"(id) NOT VALID;


--
-- PostgreSQL database dump complete
--

