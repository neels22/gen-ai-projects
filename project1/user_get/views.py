from django.http import JsonResponse

# Sample user data
users = [
    {
        "id": 1,
        "name": "neel",
        "email": "abc@gmail.com"
    },
    {
        "id": 2,
        "name": "john",
        "email": "john@example.com"
    }
]

def get_user(request, id):
    if request.method == 'GET':
       
        for user in users:
            if user["id"] == id:              
                return JsonResponse(user)    
        return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
