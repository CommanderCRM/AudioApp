-- DDL Generated from https:/databasediagram.com

CREATE TABLE patient_table (
  card_number VARCHAR(12) PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  gender CHAR(1) NOT NULL,
  constant_password VARCHAR(128),
  hospital VARCHAR(64) NOT NULL,
  temporary_password VARCHAR(128),
  is_password_changed BOOL NOT NULL,
  date_of_birth DATE NOT NULL,
  patient_info VARCHAR
);

CREATE TABLE signal_table (
  signal_id SERIAL PRIMARY KEY,
  signal_type VARCHAR(50) NOT NULL,
  base64_value VARCHAR NOT NULL,
  base64_segment_value VARCHAR,
  is_reference_signal BOOL NOT NULL,
  real_value VARCHAR(50) NOT NULL
);

CREATE TABLE signal_compare_table (
  signal_compare_id SERIAL PRIMARY KEY,
  compared_signal_id_1 INT REFERENCES signal_table(signal_id) NOT NULL,
  compared_signal_id_2 INT REFERENCES signal_table(signal_id),
  compared_signal_id_3 INT REFERENCES signal_table(signal_id),
  signal_score REAL
);

CREATE TABLE session_table (
  session_id SERIAL PRIMARY KEY,
  is_reference_session BOOL NOT NULL,
  session_type VARCHAR(50) NOT NULL,
  card_number VARCHAR(12) REFERENCES patient_table(card_number) NOT NULL,
  session_info VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE session_compare_table (
  session_compare_id SERIAL PRIMARY KEY,
  compared_session_id_1 INT REFERENCES session_table(session_id) NOT NULL,
  compared_session_id_2 INT REFERENCES session_table(session_id),
  compared_session_id_3 INT REFERENCES session_table(session_id),
  session_score REAL
);

CREATE TABLE signal_session_table (
  signal_session_id SERIAL PRIMARY KEY,
  signal_id int REFERENCES signal_table(signal_id) NOT NULL,
  session_id int REFERENCES session_table(session_id) NOT NULL
);

CREATE TABLE doctor_table (
  username VARCHAR(255) PRIMARY KEY,
  specialization VARCHAR(255) NOT NULL,
  hospital VARCHAR(64) NOT NULL,
  password VARCHAR(128) NOT NULL,
  full_name VARCHAR(255) NOT NULL
);

CREATE TABLE specialist_table (
  username VARCHAR(255) PRIMARY KEY,
  password VARCHAR(128) NOT NULL,
  specialist_info VARCHAR
);

CREATE TABLE doctor_patient_table (
  doctor_patient_id SERIAL PRIMARY KEY,
  doctor_username VARCHAR(255) REFERENCES doctor_table(username) NOT NULL,
  patient_card_number VARCHAR(12) REFERENCES patient_table(card_number) NOT NULL
);

CREATE TABLE syllables_phrases_table (
  syllable_phrase_id SERIAL PRIMARY KEY NOT NULL,
  syllable_phrase_type VARCHAR(10) NOT NULL,
  dict VARCHAR(10) NOT NULL,
  value VARCHAR(50) NOT NULL
);

CREATE TABLE refresh_token_table (
  refresh_token_id SERIAL PRIMARY KEY,
  token UUID NOT NULL,
  username VARCHAR(255) NOT NULL,
  exp INT NOT NULL,
  role VARCHAR(20) NOT NULL
);

INSERT INTO doctor_table VALUES ('user0', 'logoped onkolog', 'Tomsk NII', 'aca8d61fe60d8d9c5c6efe801df4e66706b23dae45224607a414c41126c8f0b847fe4d0366b409f7698bf00ebfc495bc2cafc45807c3e489d4a23a2ee5d57638', 'Evgenij Ivanov');
INSERT INTO doctor_table VALUES ('user1', 'logoped onkolog', 'Tomsk NII', '5820de135352b89fa85a1c20505917a91c114476697903219648a1c7057f9803b6160cc2e0b6ca3c23ea3bcdf49968aa4bc960f9f4ad48f1c08bd19951b04f32', 'Denis Smirnov');
INSERT INTO doctor_table VALUES ('user2', 'logoped onkolog', 'Tomsk NII', '1c35eb57c2fd7b6e095d3543751f1822ee696c7b6521a29b218714ee881279df043f28441cfe15792f2515b9a2d004fcc2c46fcfff8d0b049ef32f40e1b81339', 'Anton Kuznetsov');
INSERT INTO doctor_table VALUES ('user3', 'logoped onkolog', 'Tomsk NII', '84754c158b68e69e4d3e3c4f056cd62421c0213fdaab448f912d79d7229267c6252e6c37618f73f9bde7adc9b2c0b790029cb038c132c2f904a644574a42b22d', 'Igor Popov');
INSERT INTO doctor_table VALUES ('user4', 'logoped onkolog', 'Tomsk NII', '0a5d23378bdcf3695ead8964b95b6287644ef07146747ca928555b9102f2c92ab601879907fe07b48efdb34fe65a0813cf415e77c2425dc10c6f3e4abda5a2a8', 'Jurij Vasilev');
INSERT INTO doctor_table VALUES ('user5', 'logoped onkolog', 'Tomsk NII', '49aa16561666bdc50c69b51c3f3762c2072c5085c3bd16d8a7e6308e008c47ef355e2e927be5785df78a3f3e7ca3e0a0a0fd65c19304b8932dce24117a291bf5', 'Oleg Petrov');
INSERT INTO doctor_table VALUES ('user6', 'logoped onkolog', 'Tomsk NII', 'aa8a69f884759b7e972bd7c2b8c0591ea1a0f93a425b2fbf374dd6cdfb42e6aabe5c41297bf4f9f77e98b39b6d3e259f384dda580a713be3335f138e1bfb9c81', 'Vjacheslav Sokolov');
INSERT INTO doctor_table VALUES ('user7', 'logoped onkolog', 'Tomsk NII', '5e0b0cea5cf12f918cc7bfc9a97677a1ce541941a4e686aa5c7fd139de79f02a520ed227c6f696682b45cf78b7da49e92e27c5bf5348389732d0f51b44b3d122', 'Vasilij Mihajlov');
INSERT INTO doctor_table VALUES ('user8', 'logoped onkolog', 'Tomsk NII', '4a752cd159c31d5fda0d6e1dfbe994abe921f8b0b9be1ed49c3cfe7475a966c38e8f1f877f3be4ea09aa6637f7681cc84b5c83a7eb9e9d8129738b4eda86f121', 'Stanislav Novikov');
INSERT INTO doctor_table VALUES ('user9', 'logoped onkolog', 'Tomsk NII', '084253f28220ede5bab03a25fc3d48d214b7493013a58625111a3a65c00a93fd1c40648d34a0476eee0ff4dc2323dd07800a6a8b32acc5787819fb8116096eca', 'Vadim Fedorov');
INSERT INTO doctor_table VALUES ('user10', 'logoped onkolog', 'Tomsk NII', '59e5058a9ac6080cbc552c563844826774b73965fdf04ed3e6be652062e35fc86f3108c37af031b3398b72f2c6e756fad4664f73773c4ddff3330c0fcbf7b29e', 'Elena Koneva');
INSERT INTO doctor_table VALUES ('user11', 'logoped', 'Moscow NII_1', '84ead26caf7a79ea3fcd66ebe173d9b33c8f727727c3503a47df2377cf40f05d184baa10e2f9aa509937842619ac33249118920bb875ca0b29fb0f3dd793fae7', 'Natalja Poljanskaja');
INSERT INTO doctor_table VALUES ('user12', 'logoped', 'Moscow NII_1', 'de70cd5800928076bc7dbd3617df1dca2d00f5a5be137b71ee8fe5773765f82a292c5a417de980902f503f49a4127538e22783606c8f5f6960dbf469cb3b6d13', 'Olga Snegova');
INSERT INTO doctor_table VALUES ('user13', 'logoped', 'Moscow NII_1', '9d9609bdd72bdf0dc6cb1ea75f439d6e5cacfbaabfe7df1954ba1028f7e8622b39f8a199ce22b3d3ac8386cf3ce61f534848c8f587566994f17a27ba08629c1a', 'Julija Karpova');
INSERT INTO doctor_table VALUES ('user14', 'logoped', 'Moscow NII_1', 'a0716871ddd002d7c04381c9c154b842d3eb0f32269b11038dcbc6836b462d45da4535a9b7099e54e069243868f8f348cf9a6be468ea68fa03e7efbb0a109adc', 'Tatjana Matveeva');
INSERT INTO doctor_table VALUES ('user15', 'logoped', 'Moscow NII_1', '37d29ab64d506168b5fb208391f207f5eb186166f06642fab3290e7f3b48d2f8c730b401af2e7f4aa33d21a67cf7e1f5d1e2e3b5cf17c8b432f37c8243459f24', 'Irina Medvedeva');
INSERT INTO doctor_table VALUES ('user16', 'logoped', 'Moscow NII_1', '3585fed3201d6f1b53ce345934af90ce5ed582622b994979a2226a9507669927f7ffede576713b85b27dc40479a38d56d07ca6dfc1922e7aa1a9b3a16367b2cb', 'Svetlana Belaja');
INSERT INTO doctor_table VALUES ('user17', 'logoped', 'Moscow NII_1', '1a2512d93ac51233d5f452c255213a37974132aea27a1f8aed833cc81776dd32dfc7ff8230647a8e9668c67136822d018e9dcda283c604575c78bb849a67015d', 'Marina Poljakova');
INSERT INTO doctor_table VALUES ('user18', 'logoped', 'Moscow NII_1', '7621dc4101d83b2b6124b861781397c493e8b656bd424204471e4442af010a40b2bb7f4a89fe0dc100a7bd35e1d605935cac1c36192bc343f6caf9cd42b58d3a', 'Nadezhda Frolova');
INSERT INTO doctor_table VALUES ('user19', 'logoped', 'Moscow NII_1', 'd14f41365c0edf3c855d5f300ffdb9fb2438b7438fd0caf43032ad4447562f5532d0990bbb6639da3ec9569f931d9036ef9f7feb212281c26ae63ed1513fda09', 'Ljubov Levchenko');

INSERT INTO specialist_table VALUES ('user21', 'aad5b917d3963499d57725d8b18bad6eec4c397afc687e2cb9ad9e33167344ac3432226de632a5e8ed639762448c4aaed3f2327fd1ff40f9692080b26112b048');
INSERT INTO specialist_table VALUES ('user22', 'c193b8e2ee7525fd91879cf6846ae2495ec674984676f4f2958b319a0d3430492563233c6b1f12d60cc051975ce278c6ab5f8ab3fd058ebc3445fe08c859c5b5');
INSERT INTO specialist_table VALUES ('user23', '3dc22c3d586d786232b2b860a323ceb0e881809f3e61f742d8dcd3910b414c36920fe33e8ade3325baaf07d1a10d9ceb2032b1cdedef21fcc25627e6eefcb306');
INSERT INTO specialist_table VALUES ('user24', '3b59bf04379ede032a15d007e65509c3ffcb7ee6aa282e7c75b5d42dc346e5ce22c4793687d0dfb3fff9e9257b60b765a8da4f2b43c5cfde18d7138796e630f2');
INSERT INTO specialist_table VALUES ('user25', '42bc36049f98c95d43f5abbfc031867cbb789e3da25f82b4973133eacddad9b93606892d81a835f3f7503b17fe742cf19eb8f9c34381d36b2a2b15f4e353e0bc');
INSERT INTO specialist_table VALUES ('user26', '8bd7a72e6c42e1ab9c10d30ef8ffd825ee555a9bcb8e76c600d75a72afb83fa995387d380690687d72ac21e42c5495146090a00ff63930f7986e58ebc3019289');
INSERT INTO specialist_table VALUES ('user27', 'd8dcfc61d125b2ab404af0ba6602cebbd5e8904f6b61f66224c6dff9b1c0b5b85cfe35eb8f54ab7c306f9543fac8681e4f569ff1f2877a5b41c5dad570b9b247');
INSERT INTO specialist_table VALUES ('user28', '88d267bd387ac0ba62bdbce7e991701e12bdc64460bffcf9114e42badebfa7e924284d044e4792ccf0b3c76554efd35e608f489910e80f4a3bf404d920143198');
INSERT INTO specialist_table VALUES ('user29', '0099eca200dea718c38983acbc97fb32012a871f6d3503a83aa3d2e836216dd667b82a30930300a2de8f5b6b820e6e2def16ab3f774d7ef6d5580a9af11ffeef');
INSERT INTO specialist_table VALUES ('user30', '7858a2adc170e4790b05d52ee71f6e37532957d566d1c875c37ed3383f1da06c8262724eafb10034b134f056bb690848aa274a21adb155826a57779e06debd90');
INSERT INTO specialist_table VALUES ('user31', '72a75984156ee1699a8fc06955f543d5f9f21c702f74793cb1edc3e297af6cfbf7632ea8d8500848812cae4c9343603e04c42cf632361ab1038d065d8a60ced1');
INSERT INTO specialist_table VALUES ('user32', '020866687c4686b1145ffeb479c176833ebd50157d53b9a4af3331df77dc474bc9a2028a1ac29d742f18df64afca3605bc44ec1828fa495a5385eb9675f6d3c4');
INSERT INTO specialist_table VALUES ('user33', 'b2114c20136774156e007fceec766c4cb1852e53bfc8d08a158ed227bf09d9abaec80fdce2f89ce0fa9b54172529ed1e3f3a50923ab34f283461224650b49e13');
INSERT INTO specialist_table VALUES ('user34', '2bf7c01c3cb51db8b450f5e6687d6b572c9e8ebc4f1d696f0817ffd551db0bcd0010cd2c7c275e0cbae84736d3624d26fad453832ef022e2695e20be6bf6c7d9');
INSERT INTO specialist_table VALUES ('user35', '0b3cd17be96521eea5bd0cb42a1aa1af81c88b2376534d852b33edd9abaf57cd421fcb429c80a62bc14398abf8add47a3cda23cd5aeeb0281d9c2861fb20a5fd');
INSERT INTO specialist_table VALUES ('user36', 'e00b1180e79fec6c92164f21680c9b969bcbbd06f08ee70d1cfe29b79e7babff03b5509b19766645879da2e1c361e759d52e9bd3d3c75fcd435275a3f48c9789');
INSERT INTO specialist_table VALUES ('user37', 'c3358b4b67beeed611ac49daa9b9a6f2958ba27616352149fcb7e68d2210da2d9e603a08a239eb8972c04f448a81b0fb4e8fef57a425da892122304c5dc45f4e');
INSERT INTO specialist_table VALUES ('user38', 'fae009a613a0fdd4c87005887acdb1ca2d59a651140b3af1a65f0a815b4fc2ed5311af424b9f1a27e97fad4f50f262f17e883bc258e203a5a60c19e0a5200974');
INSERT INTO specialist_table VALUES ('user39', '01bee16f10f38e834a32f7e2be63da12847a564c222a81a8208c74ed7e41292f5d4c08f9bec0ea131afab75fc2d66a593404f42f49d555253c3c3a8fe5b9e2f2');

INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRgZ6AABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRh4HkAAAAAAAD+//////8BAP///////wAAAAD+/wAAAAAAAAAAAAAAAAAA/////wMA//8BAAAA//8BAP//AQABAAAAAAABAA', '0', 'Белая пелена лежала на полях');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRuZdAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhwF0AAP//AwABAAIAAgABAAIA//8AAP///v//////AQAAAAIABAAAAAEAAAABAAAA//8BAP//AAD+////AQD//wIAAgACAA', '1', 'В школу приезжали герои фронта');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRoZUAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhYFQAAAAA//8AAAAAAAAAAP//AAABAAAA//8AAAAAAQD//wAAAQABAAAAAQAAAP//AAAAAAAAAAAAAAAAAQD+/wAA//8AAA', '1', 'Белый пар расстилается над лужами');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRgZ6AABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRh4HkAAAEAAQABAAEAAAABAAAAAAAAAAEAAAAAAAAAAQABAAAAAAAAAAAAAQAAAAEAAQD//wEAAAAAAAAAAAD//wAAAAAAAP', '0', 'Экипаж танка понял задачу');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRqZwAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhgHAAAP////8AAAMAAgABAAIAAgD//wEABAD///z/AAABAAAAAAACAAIAAAAAAP///f8CAAQAAQABAAQAAgAAAP3//v////', '1', 'Этот блок работает хорошо');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRuZdAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhwF0AAAAAAQACAAEAAQACAAAAAQAAAAAAAAAAAAAAAAAAAAEAAQABAAAAAAAAAAAAAAABAAEAAgABAAAAAAAAAP////8AAA', '1', 'Начинаются степные пожары');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRiZLAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhAEsAAP//AAAAAAMABAAEAAUABQAGAAQABAADAAUABwAFAAYACwAIAAgABwAKAAYABAAFAAMAAQACAAMAAwABAAIAAAD+//', '0', 'Ученики поливают огород');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRkZnAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhIGcAAAAA//8AAAAAAAAAAAAA//8AAAAA//8AAAAAAAABAP//AAAAAAAAAAAAAAEAAAABAAAAAAABAAAAAAABAAAAAQAAAP', '1', 'Тяжелый подъем закончился');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRkZnAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhIGcAAPn/9f/2//T/8v/2//n/+v///wQABQAHAAkABgADAAIA/f/4//n/9f/0//j/+//8/wMABgAIAAkACwAHAAYABQABAA', '1', 'Тропинка уперлась в глинистый уступ');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRkZnAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhIGcAAP//AAAAAAAA///9//7////+//7//v/+//////8AAAAAAAABAAAAAAD//////////wEAAQAAAAEA/v//////AAD///', '0', 'Солнце поднялось над лесом');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRuZdAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhwF0AAAAAAAAAAP////8BAAAAAAABAAAAAAAAAAEAAAAAAAAAAQD//wEAAAAAAAEAAAAAAAEAAAAAAAAAAQAAAAAA/////w', '1', 'В подъезде стояли санитары');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRkZnAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhIGcAAAAAAAD//wAA//8AAAAAAQAAAAAAAQAAAAAAAAABAAAAAAD//wEA//8AAAAAAAABAAAAAQAAAAAAAAAAAAAA//8AAP', '1', 'Стало известно место встречи');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRoZUAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhYFQAAAAAAgABAAAAAwADAAMAAwACAP7///8CAAEAAQABAAIAAQACAAMAAgADAAMABAACAAIAAQAEAAMAAAACAAMAAwD//w', '0', 'На участке ведется наблюдение');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRqZwAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhgHAAAAAAAAAAAAEAAAAAAAAA//8BAAAAAAABAAAAAQAAAAAAAAABAAAAAAAAAAAAAQABAAEAAAABAAAAAAAAAAAAAAAAAA', '1', 'В класс вошел преподаватель');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRiZLAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhAEsAAAAAAQACAP//AwAAAAEAAgAAAAMAAQAAAAMAAAADAAAA//8DAP//AAACAP7/AgAAAAIAAAD//wIA/v/+/wEAAQD+/w', '1', 'Полено раскололось надвое');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRkZnAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhIGcAAP//AAD//wAAAAAAAAAAAAAAAAAAAAD//wAA//8AAP//AAAAAAAAAQAAAAAAAAAAAAAAAAAAAP//AAAAAAAA//8AAA', '0', 'Надо зарядить ружье');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRuZdAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhwF0AAAAAAQABAAAAAAAAAAEAAQABAAAAAQAAAAEAAQAAAAEAAQAAAAAAAQAAAAAAAAAAAAAAAAAAAAAA//8BAAEAAAD//w', '1', 'Телега начала скрипеть');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRuZdAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhwF0AAP////8AAP///P/+////AAD8//z/AQD///3//v8BAAAA/v///wEAAQD///////8AAP///v8BAP//AAD//wAA//8AAA', '1', 'Мать отвела ребенка в сад');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRoZUAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhYFQAAAAA/v8AAAEAAAAAAAAA//8AAAAAAAABAAAA//8AAP////8AAAAAAQAAAAAAAAABAAEAAAAAAAAAAQD//wAA//8AAA', '0', 'Ребята сидели на берегу');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRuZdAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhwF0AAAEAAQABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAEAAAABAA', '1', 'В магазине продаются яблоки');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRqZwAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhgHAAAOv/FgAGAOH/FQARANz/EgARAOL/BQAWAOn/9f8bAO//8P8dAPr/8v8VAAYA6/8MAAoA6P8JAAwA7/8BAA4A8P8CAA', '1', 'Директор сравнил доход с расходом');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRkZnAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhIGcAAAAA//8AAAAA//8AAAAA////////AAAAAP//AAD//////////wAA//8AAP////8AAP//AAD//////////wAAAAD///', '0', 'Высокая рожь колыхалась');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRmaDAABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRhQIMAAP///v/9/wEA//8BAAEA/P/9//3//v8CAAAA//8AAP7///8DAAEA///8//z/+//+//7//P////v/AAABAAEAAAD+//', '1', 'Цветы пестрели в долине');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRgZ6AABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRh4HkAAAEAAAACAAAA/v8BAP7///8BAP////8AAAAAAQACAAAAAQAAAAAAAAACAAEAAAABAAEAAQAAAAAAAAAAAP//AAD+//', '1', 'Чудный запах леса освежает');
INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', 'UklGRgZ6AABXQVZFZm10IBIAAAABAAEA4C4AAMBdAAACABAAAABkYXRh4HkAAAAAAAAAAAAAAAD//wAAAQAAAAAAAAAAAAAAAAABAAEA//8AAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAP', '0', 'День был удивительно хорош');

INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Белая пелена лежала на полях');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В школу приезжали герои фронта');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Белый пар расстилается над лужами');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Экипаж танка понял задачу');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Этот блок работает хорошо');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Начинаются степные пожары');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Ученики поливают огород');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Тяжелый подъем закончился');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Тропинка уперлась в глинистый уступ');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Солнце поднялось над лесом');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В подъезде стояли санитары');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Стало известно место встречи');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','На участке ведется наблюдение');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В класс вошел преподаватель');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Полено раскололось надвое');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Надо зарядить ружье');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Телега начала скрипеть');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Мать отвела ребенка в сад');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Ребята сидели на берегу');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В магазине продаются яблоки');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Директор сравнил доход с расходом');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Высокая рожь колыхалась');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Цветы пестрели в долине');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Чудный запах леса освежает');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','День был удивительно хорош');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('syllable','[к]','кась');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('syllable','[к`]','кясь');

SELECT * FROM doctor_table;
SELECT * FROM syllables_phrases_table;
