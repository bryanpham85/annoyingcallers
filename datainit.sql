--INSERT INTO public.ac_category
--(id, "name", category_type, created_date)
--VALUES (nextval('ac_category_id_seq'::regclass), 'Insurance', 2, Now()),
--(nextval('ac_category_id_seq'::regclass), 'RealEstate', 2, Now());
--
--INSERT INTO public.ac_registered_device
--("deviceId", "devicePlatform", installed_date, owner_id)
--VALUES('idfa123', 'iOS', Now(), null),
--VALUES('aaid123', 'Android', Now(), null);

--INSERT INTO public.ac_caller
--("callerId", country_code, caller_number, registered_date, registered_by_id)
--values
--(nextval('"ac_caller_callerId_seq"'::regclass), '+84', '11111111111', Now(), 'aaid123'),
--(nextval('"ac_caller_callerId_seq"'::regclass), '+84', '99999999999', Now(), 'idfa123');

INSERT INTO public.ac_caller_category
(id, caller_id, category_id)
values
(nextval('ac_caller_category_id_seq'::regclass), 5, 1),
(nextval('ac_caller_category_id_seq'::regclass), 6, 3);

