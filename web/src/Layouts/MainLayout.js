import { Outlet } from "react-router-dom"
import MyNav from "../Components/MyNav"
import Alert from "../Hooks/Alert";

const MainLayout = () => {
    return (
        <>
            <MyNav />
            <Outlet />
            <Alert />
        </>
    );
}

export default MainLayout;