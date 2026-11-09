from url_ast import generate

from collections import ChainMap
import pprint
# More memory efficient
# "zero length" element, but hash still stored in the map (?)
#set := make(map[string]struct{})
#set["apple"] = struct{}{}
#set["banana"] = struct{}{}

# Check for existence
#if _, ok := set["apple"]; ok {
    #// exists
#}

#make "max element url" a variable for each
#   "step" in the api 

"""
import "fmt"

type access interface {
	parse()
}

func test() {
	fmt.Println("see me jump")
}

func test2() {
	fmt.Println("see me run")
}

type url_tree struct {
	tree     map[string]url_tree
	callback map[string]interface{}
}

func main() {

	tree_ex := url_tree{
		tree: map[string]url_tree{
			"next": {
				tree: map[string]url_tree{},
				callback: map[string]interface{}{
					"GET":  test,
					"POST": test2,
				},
			},
		},
		callback: map[string]interface{}{},
	}

	for true {
		if val, ok := tree_ex.tree["next"]; ok {
			// endpoint/tree exists, pass on request
			tree_ex = val
		} else {
			// return 404
			break
		}
	}
	tree_ex.callback["GET"].(func())()
}
"""

#zero allocation programming
    #https://medium.com/@ksandeeptech07/zero-allocation-in-go-ce29e6a9ffdc
    #https://go.dev/doc/gc-guide#Understanding_costs
    #https://gchandbook.org/
    
        #prebatch alloc

#https://www.digitalocean.com/community/tutorials/how-to-make-an-http-server-in-go#using-middleware-to-process-requests
    #add basic types
        #add unknown endpoint/method handling
            #logging

#get roots (i.e. "_matrix", "_board", etc.)
    #custom handler
    #   https://dev.to/jones_charles_ad50858dbc0/building-high-performance-http-servers-with-gos-nethttp-4413
    #for each root, generate a "http.Handle("/{root}", new(countHandler))"
    #   "countHandler" struct for things like DB connection and other shared
    #   connections
    #

"""
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        fmt.Printf("started %s %s\n", r.Method, r.URL.Path)

        next.ServeHTTP(w, r)

        fmt.Printf("completed %s %s\n", r.Method, r.URL.Path)
    })
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", getRoot)
    mux.HandleFunc("/hello", getHello) 

    loggedMux := loggingMiddleware(mux)

    err := http.ListenAndServe(":3333", loggedMux)
    if err != nil {
        fmt.Printf("error starting server: %s\n", err)
    }
}
"""

if __name__ == "__main__":
    temp_ret = generate()
    ret_val = temp_ret.pop()
    for i in temp_ret:
        ret_val = dict(ChainMap(ret_val, i))

    def iterate(named: dict):
        for key in named.keys():
            if type(named[key]) == type(dict()) and "method" in named[key].keys():
                # create file/dir
                # replace "." with "_"
            else:
                try:
                    os.mkdir(key.replace(".", "_").replace("{", "_").replace("}", "_"))
                except:
                    pass
                os.chdir(key)
                iterate(named[key])
                os.chdir("..")

    iterate(ret_val)

    with open("output.txt", "w") as out:
        pprint.pp(ret_val["tree"], stream=out)
    