def getdashboardurl(user):
    if user.role == 1:
        dashboardurl = "vendordashboard"
    elif user.role == 2:
        dashboardurl = "customerdashboard"
    elif user.role is None and user.is_superadmin:
        dashboardurl = "/admin-panel"

    return dashboardurl
