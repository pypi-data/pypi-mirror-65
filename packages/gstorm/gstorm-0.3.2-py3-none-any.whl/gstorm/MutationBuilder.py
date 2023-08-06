from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import inflect
from pygqlc import GraphQLClient
from gstorm.BaseGraphQLType import BaseGraphQLType
from gstorm.enums import QueryType
from gstorm.helpers.str_handling import remove_capital, contains_digits
from gstorm.helpers.date_helpers import get_utc_date, get_iso8601_str
from gstorm.helpers.gql import setup_gql

'''
# ! EXAMPLE DATA:
prog = BbtProgram(
  guid= "BBT-PROG-123",
  bottlingDemandGuid= "BOT-123",
  initialConditionGuid= "BBT-INV-123",
  context= "{\"a\": 10, \"b\": \"b\", \"c\": []}",
  status= ProgramStatus.WAITING_APPROVAL,
  selected= False,
  programs=[
    BottlingOrderBbtProgram(
      locked=True,
      context={},
      bottlingOrder=BottlingOrder(...),
      bbtPlans=[
        BbtPlan(
          line= Line(code="LINEA001", name="Linea 1"),
          bbtTank= Tank(name="L101", type="Gobierno"),
          brightBeer= BrightBeer(code="TECATE LIGHT NACIONAL", name="Tecate light nacional"),
          volume= 1000.0,
          startAt= "2020-02-27T22:00:00Z",
          endAt= "2020-02-27T22:00:00Z",
          sequence= 1,
          usage= TankUsageType.REGULAR
        ),
        BbtPlan(
          lineCode= "LINEA002",
          bbtTankName= "L103",
          brightBeerCode= "XX LAGER",
          volume= 550.0,
          startAt= "2020-02-27T22:00:00Z",
          endAt= "2020-02-27T22:00:00Z",
          sequence= 1,
          usage= TankUsageType.REGULAR
        )
      ],
    )
  ],
  bbtDemands=[

  ]
)

# 1. Queries
inventories = BbtInventory.query()
orders = BottlingOrder.query()
# 2. planear
prog = BbtPlanner(orders, inventories)
# dentro de BbtPlanner:
def BbtPlanner():
  prog = BbtProgram()
  prog.guid = get_guid()
  # planear
  or_program = ortools.plan()
  for or_plan in or_program:
  prog.programs.append(BottlingOrderBbtProgram(or_plan))
# 3. Subir datos a BD




gstorm.upload(prog)




# 1. generar mutations
MUT = MutationBuilder(prog)
# 2. Correr mutations
result, errors = gql.mutate(MUT)
# 3. Update de objeto de Planeacion
if errors:
  prog.set_errors(errors)
  prog.set_sync(false)
else:
  prog.set_sync(true)
  prog.id = result.id
if gstorm.validate(prog):
  send_notification('success')
else:
  send_notification('error')

# ! NESTED MUTATION VERSION
mutation (
  $createPlans: [CreateBbtPlanParams]
  $createPrograms: [CreateBottlingOrderBbtProgramParams]
){
  createBbtProgram(
    guid: "BBT-PROG-123"
    bottlingDemandGuid: "BOT-123"
    initialConditionGuid: "BBT-INV-123"
    context: "{\"a\": 10, \"b\": \"b\", \"c\": []}"
    status: WAITING_APPROVAL
    selected: false
    createPlans: $createPlans
    createPrograms: $createPrograms
  ){
    successful
    messages{
      field
      message
    }
    result{
      id
    }
  }
}

# this stuff is a dictionary:
{
  "createPlans": [],
  "createPrograms": [{
    "locked": true,
    "context": "{}",
    "bottlingOrderId": 1,
    "createBbtPlans": [{
      "lineCode": "LINEA001",
      "bbtTankName": "L101",
      "brightBeerCode": "TECATE LIGHT NACIONAL",
      "volume": 1000.0,
      "startAt": "2020-02-27T22:00:00Z",
      "endAt": "2020-02-27T22:00:00Z",
      "sequence": 1,
      "usage": "REGULAR"
    }, {
      "lineCode": "LINEA002",
      "bbtTankName": "L103",
      "brightBeerCode": "XX LAGER",
      "volume": 550.0,
      "startAt": "2020-02-27T22:00:00Z",
      "endAt": "2020-02-27T22:00:00Z",
      "sequence": 1,
      "usage": "REGULAR"
    }]
  }],
  "createBbtDemands": [{
    "centerName": "MC08",
    "actorName": "APP",
    "guid": "BBT-DEM-123",
    "createBbtOrders": [{
      "bbtTankName": "L101",
      "brightBeerCode": "TECATE LIGHT NACIONAL",
      "volume": 1500,
      "minStartAt": "2020-02-27T22:00:00Z",
      "maxEndAt": "2020-02-27T23:00:30Z"
    }]
  }]
}

# ! BATCH MUTATION VERSION:
  # ! STEP 1
mutation {

}
'''

class MutationBuilder():
  pass