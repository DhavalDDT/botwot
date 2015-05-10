create table if not exists lines (
  timestamp real not null,
  name text not null,
  message text unique not null
);
