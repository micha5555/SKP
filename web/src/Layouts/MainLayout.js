import { Outlet, useNavigate } from "react-router-dom"
import MyNav from "../Components/MyNav"
import Alert from "../Hooks/Alert";
import Footer from "../Components/Footer";

const MainLayout = () => {

    return (
        <div className="height100 d-flex flex-column">
            <MyNav />
            <div className="grow">
                <Outlet />
            </div>
            <Alert />
            <Footer />
        </div>
    );
}

export default MainLayout;