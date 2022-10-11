import React from 'react';
import './style.css';
import { InventoryCard } from './InventoryCard';
import {sort} from './History';
import { Piechart } from './Piechart';
import { DashboardHT } from './DashboardHT';
import { Inventory } from './Inventory';

export function Dashboard(props) {
    let history = props.history.dispensions;
	history.sort(sort);

    return (
        <div className="dashBody">
                <div onClick={() => {
                    props.setHigh(true)
                    props.setLow(false)
                    props.setCritical(false)
                    props.activePageHandler("Inventory")
                    }}>
                    <InventoryCard title='High' mergedData={props.mergedData}/>
                </div>
                <div onClick={() => {
                    props.setHigh(false)
                    props.setLow(true)
                    props.setCritical(false)
                    props.activePageHandler("Inventory")
                    }}>
                    <InventoryCard title='Low' mergedData={props.mergedData}/>
                </div>
                <div onClick={() => {
                    props.setHigh(false)
                    props.setLow(false)
                    props.setCritical(true)
                    props.activePageHandler("Inventory")
                    }}>
                    <InventoryCard title='Critical' mergedData={props.mergedData}/>
                </div>
                <div className="footer-container">
                    <div className="hisTable" active={(props.activePage === "History").toString()}
                    onClick={() => props.activePageHandler("History")}>
                        <DashboardHT history={props.history}/>
                    </div>
                    <div className="pie">
                        <Piechart history={props.history}/>
                    </div>
                </div>
            </div>
    )
}
