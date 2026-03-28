# Database design

Travel Planner bruker en MariaDB database for å lagre informasjon om reiser og aktiviteter.

## Tabell: trips

| Felt        | Type    | Beskrivelse  |
| ----------- | ------- | ------------ |
| id          | INT     | Primærnøkkel |
| destination | VARCHAR | Reisemål     |
| start_date  | DATE    | Startdato    |
| end_date    | DATE    | Sluttdato    |

## Tabell: activities

| Felt          | Type    | Beskrivelse                |
| ------------- | ------- | -------------------------- |
| id            | INT     | Primærnøkkel               |
| trip_id       | INT     | Fremmednøkkel til trips.id |
| activity_name | VARCHAR | Navn på aktivitet          |
| activity_date | DATE    | Dato for aktiviteten       |

## Relasjon

En reise kan ha flere aktiviteter.

Relasjonen mellom tabellene er:

trips (1) → (mange) activities
