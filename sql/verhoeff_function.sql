delimiter $$
CREATE  FUNCTION `checksumVerhoeff`(`pNUMBER` bigint, `pAction` tinyint unsigned)
RETURNS tinyint(4)
BEGIN
DECLARE c tinyint unsigned;
DECLARE len int;
DECLARE m tinyint unsigned;
DECLARE n varchar(255);
DECLARE i smallint;
DECLARE t int;
DECLARE d char(100);
DECLARE p char(80);
DECLARE inv char(10);
SET d='0123456789123406789523401789563401289567401239567859876043216598710432765982104387659321049876543210';
SET p='01234567891576283094580379614289160435279453126870428657390127938064157046913258';
SET inv='0432156789';
SET c = 0;
SET n = Reverse(pNUMBER);
SET len = Char_length(rtrim(n));
set i=0;
WHILE i < len
DO
IF pAction = 1 THEN
SET m = substring(p,(((i+1)%8)*10)+ substring(n,i+1,1) +1,1); 
ELSE
SET m = substring(p,((i%8)*10)+ substring(n,i+1,1)+1,1);
END IF;
SET c = substring(d,(c*10+m+1),1);
SET i=i+1;
END WHILE;
IF pAction = 1 THEN
SET c = substring(inv,c+1,1);
END IF;
return (c);
END;
$$
