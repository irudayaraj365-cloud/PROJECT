use alwin;
create table user(user_id int primary key, username text,email text,mobile bigint,password text,created_at datetime);
create table flight (id int primary key,name text, flight_number int,departure text,arrival text,price int, available_seats int,created_at datetime);
create table hotel(id int primary key, name text, location text,price decimal(10,2),available_rooms int,created_at datetime);
create table booking(id int primary key auto_increment,user_id int,flight_id int,hotel_id int,booking_amount int,amount_paid decimal(10,2));
insert into user(user_id, username, email, mobile, password, created_at) values
(1, 'john doe', 'john@example.com', 9876543210, 'password123', now()),
(2, 'jane smith', 'jane@example.com', 8765432109, 'securepass', now()),
(3, 'alice brown', 'alice@example.com', 7654321098, 'alicepass', now()),
(4, 'mark taylor', 'mark@example.com', 6543210987, 'markpass', now()),
(5, 'lisa carter', 'lisa@example.com', 5432109876, 'lisapass', now()),
(6, 'mike johnson', 'mike@example.com', 4321098765, 'mikepass', now()),
(7, 'emily clark', 'emily@example.com', 3210987654, 'emilypass', now()),
(8, 'robert hall', 'robert@example.com', 2109876543, 'robertpass', now());
insert into flight(id, name, flight_number, departure, arrival, price, available_seats, created_at) values
(1, 'air india', 'AI202', 'delhi', 'mumbai', 5000, 150, now()),
(2, 'indigo', '6E101', 'bangalore', 'chennai', 4000, 120, now()),
(3, 'spicejet', 'SG303', 'hyderabad', 'kolkata', 4500, 100, now()),
(4, 'vistara', 'VT404', 'chennai', 'delhi', 5500, 90, now()),
(5, 'go air', 'GA505', 'mumbai', 'hyderabad', 4800, 110, now()),
(6, 'air asia', 'AA606', 'kolkata', 'bangalore', 4200, 130, now()),
(7, 'emirates', 'EK707', 'dubai', 'delhi', 9500, 60, now()),
(8, 'qatar airways', 'QR808', 'doha', 'mumbai', 8800, 75, now());
insert into hotel (id, name, location, price, available_rooms, created_at) values
(1, 'taj mahal hotel', 'mumbai', 8000.00, 50, now()),
(2, 'leela palace', 'bangalore', 7500.00, 40, now()),
(3, 'hyatt regency', 'chennai', 7000.00, 60, now()),
(4, 'marriott', 'delhi', 9000.00, 55, now()),
(5, 'radisson blu', 'hyderabad', 8500.00, 45, now()),
(6, 'westin', 'kolkata', 7800.00, 35, now()),
(7, 'grand hyatt', 'dubai', 11000.00, 70, now()),
(8, 'jw marriott', 'doha', 10500.00, 65, now());
insert into booking (user_id, flight_id, hotel_id, booking_amount, amount_paid) values
(1, 1, 1, 13000, 13000.00),
(2, 2, 2, 11500, 11500.00),
(3, 3, 3, 11500, 11500.00),
(4, 4, 4, 14500, 14500.00),
(5, 5, 5, 13300, 13300.00),
(6, 6, 6, 12000, 12000.00),
(7, 7, 7, 20500, 20500.00),
(8, 8, 8, 19300, 19300.00);
DELIMITER //
create procedure book_trip(
in uid int,
in fid int,
in hid int,
in b_date date
)
BEGIN
declare seats int;
declare rooms int;
select available_seats into seats from flights where id=fid;
select available_rooms into rooms from flights where id=hid;
if seats>0 and rooms>0 then
insert into booking(user_id,flight_id,hotel_id,booking_date)values(uid,fid,hid,b_date);
update flights set available_seats=available_seats-1 where id=fid;
update hotel set available_rooms=available_rooms-1 where id=hid;
else
 signal sqlstate '45000' set message_text='No Seats or Room Available';
end if;
end //
DELIMITER ;

DELIMITER //
create procedure calculate_cost(in booking_id int,out total_cost decimal(10,2))
begin
select f.price+h.price into total_cost from booking b
join flights f on b.flight_id=f.id
join hotel h on b.hotel_id=h.id
where b.id=booking_id;
end //
DELIMITER ;

DELIMITER //
create trigger check_availablity before insert on booking for each row
begin
declare seats int;
declare rooms int;
select available_seats into seats from flights where id=new.flight_id;
select available_seats into seats from flights where id=new.flight_id;
if seats<0 then
signal sqlstate '45000'set message_text='No Available Seats on Flight';
end if;
if rooms<=0 then
signal sqlstate '45000'set message_text='No Available rooms on Hotel';
end if;
end //
DELIMITER ;

DELIMITER //
create trigger check_amount before insert on booking for each row
begin
declare total decimal(10,2);
select f.price + h.price into total
    from flights f, hotel h
    where f.id = new.flight_id and h.id = new.hotel_id;
if new.amount_paid <> total then
signal sqlstate '45000' set message_text='Incoorect Amount Paid';
end if ;
end //
DELIMITER ;

select b.id as booking_id, b.booking_date,u.user_id, u.username, u.email, f.id as flight_id, f.flight_number, f.price as flight_price, h.id as hotel_id, h.name as hotel_name, h.location, h.price as hotel_price, 
b.booking_amount, b.amount_paid from booking b
inner join user u on b.user_id = u.user_id
inner join flight f on b.flight_id = f.id
inner join hotel h on b.hotel_id = h.id;

select h.name from hotel h
where h.id = (select hotel_id from booking group by hotel_id order by count(*) desc limit 1);

select user_id from booking group by user_id having count(*) > 1;










































