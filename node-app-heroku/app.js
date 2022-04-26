/**
 * Here we are importing the `neo4j` object from the `neo4j-driver` dependency
 */
// tag::import[]
// Import the neo4j dependency from neo4j-driver
const neo4j = require('neo4j-driver')
// end::import[]

const express = require('express')
const path = require('path')
//const {fileURLToPath} = require('url')

const username = 'neo4j'
const password = 'bSsQ-_vuA9R0Yc73QlVsjztvcAMHZHCLHFsCAe4YCxY'
const connectionString = 'neo4j+s://9c453c0d.databases.neo4j.io'
const driver = neo4j.driver(connectionString,
  neo4j.auth.basic(username, password))

//const __filename = fileURLToPath(import.meta.url);
//const __dirname = path.dirname(__filename);
var app = express();
app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
    console.log(path.join(__dirname, 'index.html'));
});
app.use('/src/:id', function (req, res) {
    res.sendFile(path.join(__dirname, '/src/' + req.params.id));
    console.log(path.join(__dirname, '/src/' + req.params.id));
});
app.use('/read/:id', function (req, res) {
    var ms = new MyService(driver);
    console.log(path.join(__dirname, req.params.id));
    ms.method(req.params.id).then(function(result) {
     const records = []
     for (rec of result['records']){
        records.push(rec['_fields'][0]['properties']['name'])
    }
     console.log(records)
     res.send(records)
    })
});
app.listen(process.env.PORT || 4000, function () {
    console.log('Node app is working!');
});


//How to make get request??
//Route request to read
//Return the results of the database query

/**
 * We may also need access to the session variable to set the default session mode
 * on the session object (session.READ or session.WRITE).
 * See #sessionWithArgs

// tag::importWithSession[]
import neo4j, { session } from 'neo4j-driver'
// end::importWithSession[]
*/

/**
 * Example Authentication token.
 *
 * You can use `neo4j.auth` to create a token.  A basic token accepts a
 * Username and Password
 */
//const username = 'neo4j'
//const password = 'bSsQ-_vuA9R0Yc73QlVsjztvcAMHZHCLHFsCAe4YCxY'
//const connectionString = 'neo4j+s://9c453c0d.databases.neo4j.io'

// tag::auth[]
neo4j.auth.basic(username, password)
// end::auth[]

/*
 * Here is the pseudocode for creating the Driver:

// tag::pseudo[]
const driver = neo4j.driver(
  connectionString, // <1>
  authenticationToken, // <2>
  configuration // <3>
)
// end::pseudo[]

The first argument is the connection string, it is constructed like so:

// tag::connection[]
  address of server
          ↓
neo4j://localhost:7687
  ↑                ↑
scheme        port number
// end::connection[]
*/

/**
 * The following code creates an instance of the Neo4j Driver
 */
// tag::driver[]
// Create a new Driver instance
//const driver = neo4j.driver(connectionString,
//  neo4j.auth.basic(username, password))
// end::driver[]


/**
 * It is considered best practise to inject an instance of the driver.
 * This way the object can be mocked within unit tests
 */
class MyService {
  driver

  constructor(driver) {
    this.driver = driver
  }

  method(id) {
    // tag::session[]
    // Open a new session
    const session = this.driver.session()
    // end::session[]

    const res = session.readTransaction(tx => {
      console.log('Reading')
      return tx.run(
        `MATCH (n)--(k) WHERE n.name = $name
        RETURN k
        LIMIT 50`,{name: id} // <2>
      )
    })

    return res.then(function(result) {
     //console.log(result['records']) // "Some User token"
     return result
    })
    //console.log(res)

    //return res.records
    // Do something with the session...

    // Close the session
    session.close()
  }
}

/**
 * These functions are wrapped in an `async` function so that we can use the await
 * keyword rather than the Promise API.
 */
const main = async () => {
  // tag::verifyConnectivity[]
  // Verify the connection details
  await driver.verifyConnectivity()
  // end::verifyConnectivity[]

  console.log('Connection verified!')

  // tag::driver.session[]
  // Open a new session
  const session = driver.session()
  // end::driver.session[]

  // Run a query

  const res = await session.readTransaction(tx => {
    return tx.run(
      `MATCH (n)
      RETURN n.name AS name
      LIMIT 10` // <2>
    )
  })

  

  console.log(res['records'])

  for (const Record of res['records']){
    console.log(Record['_fields'][0])
  }

  //const query = 'MATCH (n) RETURN n.name LIMIT 10'
  //const params = {}

  // tag::session.run[]
  // Run a query in an auto-commit transaction
  //const res = await session.run(query, params)
  // end::session.run[]

  // tag::session.close[]
  // Close the session
  //await session.close()
  // end::session.close[]

}



const readTransaction = async () => {
  const session = this.driver.session()

  // tag::session.readTransaction[]
  // Run a query within a Read Transaction
  const res = await session.readTransaction(tx => {
    return tx.run(
      `MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
      WHERE m.title = $title // <1>
      RETURN p.name AS name
      LIMIT 10`,
      { title: 'Arthur' } // <2>
    )
  })
  // end::session.readTransaction[]

  await session.close()
}



const writeTransaction = async () => {
  const session = this.driver.session()

  // tag::session.writeTransaction[]
  const res = await session.writeTransaction(tx => {
    return tx.run(
      'CREATE (p:Person {name: $name})',
      { name: 'Michael' }
    )
  })
  // end::session.writeTransaction[]

  await session.close()
}


/**
 * This is an example function that will create a new Person node within
 * a read transaction and return the properties for the node.
 *
 * @param {string} name
 * @return {Record<string, any>}  The properties for the node
 */
// tag::createPerson[]
async function createPerson(name) {
  // tag::sessionWithArgs[]
  // Create a Session for the `people` database
  const session = driver.session({
    // Run sessions in WRITE mode by default
    defaultAccessMode: session.WRITE,
    // Run all queries against the `people` database
    database: 'people',
  })
  // end::sessionWithArgs[]

  // Create a node within a write transaction
  const res = await session.writeTransaction(tx => {
    return tx.run('CREATE (p:Person {name: $name}) RETURN p', { name })
  })

  // Get the `p` value from the first record
  const p = res.records[0].get('p')

  // Close the sesssion
  await session.close()

  // Return the properties of the node
  return p.properties
}
// end::createPerson[]

// Run the main method above
main()