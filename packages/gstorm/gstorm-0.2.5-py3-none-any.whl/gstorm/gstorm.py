
def main():
  print('Hello, GSTORM!')
  # ! TODO: create base class for Gstorm, other classes should inherit from it
  gql = setup_gql('dev')
  # * 1: Get data:
  GET_TANKS = '{ tanks{ id name capacity } }'
  tanks_data, errors = gql.query(GET_TANKS)
  if errors:
    pprint(errors)
    return
  tanks = [Tank(**tank) for tank in tanks_data]
  # * 2: Process data:
  pprint(f'Tank count: {len(tanks)}')
  empty_tanks = [tank for tank in tanks if tank.capacity == 0]
  print('Empty tanks:')
  pprint(len(empty_tanks))
  empty_tanks[10].capacity = 1234
  pprint(empty_tanks)
  # * re-upload data:
  UPDATE_TANK = '''
  mutation UPDATE_TANK($id: Int! $tank: UpdateTankParams!){
    updateTank(
      id: $id
      tank: $tank
    ){
      successful
      messages{
        field
        message
      }
      result{
        id
        name
        capacity
      }
    }
  }
  '''
  payload, errors = gql.mutate( mutation = UPDATE_TANK, variables= {
    'id': int(empty_tanks[10].id),
    'tank': {
      'name': empty_tanks[10].name,
      'capacity': empty_tanks[10].capacity
    }
  })
  if errors:
    print(errors)
  # * STORM
  Tank = storm.getType('Tank')
  tanks = Tank.get(filter={'capacity': 0})
  tanks[-1].capacity = 1234
  tanks[-1].update()
  storm.batchUpdate([GraphqlType])
  tank = Tank()
  tank.
  for tank_batch in storm.paginate(Tank):
    for tank in tank_batch:
      


if __name__ == "__main__":
  main()