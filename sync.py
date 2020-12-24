from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class Controller(BaseHTTPRequestHandler):
  def sync(self, parent, children):
    phase = "Completed"
    #All the child resources should be successfully created in order for the parent resource to be created successfully
    for pod_name, pod in children['Pod.v1'].iteritems():
      if pod["status"]["phase"] != "Succeeded":
        phase = "Error"

    #Setting the desired status of the parent resource
    desired_status = {
      "pods": len(children["Pod.v1"]),
      "phase": phase
    }

    # Generate the desired child object(s).
    state = parent["spec"]["state"]
    desired_pods = [
      {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "name": parent["metadata"]["name"]+"-pod1"
        },
        "spec": {
          "restartPolicy": "OnFailure",
          "containers": [
            {
              "name": "test",
              "image": "httpd",
              "command": ["echo", "Current State:, %s from Pod1" % state]
            }
          ]
        }
      },
      {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
          "name": parent["metadata"]["name"]+"-pod2"
        },
        "spec": {
          "restartPolicy": "OnFailure",
          "containers": [
            {
              "name": "test",
              "image": "httpd",
              "command": ["echo", "Current State: %s, from Pod2" % state]
            }
          ]
        }
      }
    ]
    '''
      Note: The response object can only update the status of the Parent resource.
      The children field is used to specify the desired state of the child resources,
      Create this field, by assuming that each child object will be recreated using kubectl apply command.
    '''
    return {"status": desired_status, "children": desired_pods}
  def finalize(self, parent, children):
    # Release any external resources that were allocated here
    
    phase = "Terminated"
    #All the child resources should be successfully created before deleteing them
    for pod_name, pod in children['Pod.v1'].iteritems():
      if pod["status"]["phase"] != "Succeeded":
        phase = "Error"
    #Setting the desired status of the parent resource
    desired_status = {
      "pods": len(children["Pod.v1"]),
      "phase": phase
    }
    # setting the desired state of children to an empty list in the response will delete all the child objects.
    desired_pods = []
    return {"status": desired_status, "children": desired_pods}

  def do_POST(self):
    # Serve the sync() function as a JSON webhook.
    observed = json.loads(self.rfile.read(int(self.headers.getheader("content-length"))))
    if observed["finalizing"] == True:
      desired = self.finalize(observed["parent"], observed["children"])
    else:
      desired = self.sync(observed["parent"], observed["children"])

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(desired))

HTTPServer(("", 80), Controller).serve_forever()