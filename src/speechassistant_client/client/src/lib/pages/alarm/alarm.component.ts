
import {Component, Input, OnInit, TemplateRef, ViewChild} from "@angular/core";
import {Alarm} from "../../data-access/models/alarm";
import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";
import {Title} from "@angular/platform-browser";
import {ActivatedRoute} from "@angular/router";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {AlarmStore} from "../../data-access/service/alarm.store";

@Component({
  selector: 'alarm',
  templateUrl: './alarm.component.html',
  styleUrls: ['./alarm.component.scss']
})
export class AlarmComponent implements OnInit{

  @Input() alarm: Alarm;

  @ViewChild('alarmChangeRepeating') createRepeatModal: TemplateRef<any>;
  @ViewChild('alarmChangeText') createTextModal: TemplateRef<any>;
  repeatingModalRef? : BsModalRef;
  textModalRef?: BsModalRef;

  // public mode: PickerInteractionMode = PickerInteractionMode.DropDown;

  constructor( private alarmStore: AlarmStore,
               private titleService: Title,
               private route: ActivatedRoute,
               private modalService: BsModalService ) {
  }

  ngOnInit() {
    this.titleService.setTitle('Wecker');
    this.route.params.subscribe(params => {
      this.alarmStore.getAlarm(params['id']).subscribe(alarm => this.alarm = alarm);
    });
  }

  onDeleteAlarm( id: number ): void {
    this.alarmStore.deleteAlarm( id );
  }

  onChangeAlarm( alarm: JsonObject ): void {

  }

  onChangeActivationAlarm( id: number, active: boolean ): void {
    this.alarmStore.updateAlarmActiveStatus( id, active );
  }

  openRepeatingModal(): void {
    this.repeatingModalRef = this.modalService.show(this.createRepeatModal);
  }

  openTextModal(): void {
    this.textModalRef = this.modalService.show(this.createTextModal);
  }

  closeRepeatingModal(): void {
    this.modalService.hide(this.repeatingModalRef?.id);
  }

  closeTextModal(): void {
    this.modalService.hide(this.textModalRef?.id);
  }

  closeAllModals(): void {
    this.modalService.hide(this.repeatingModalRef?.id);
    this.modalService.hide(this.textModalRef?.id);
  }

  getTimeString(alarm: Alarm): string {
    let time: Date = alarm.time;
    let hours: string = time.getHours().toString().padStart(2, '0');
    let minutes: string = time.getMinutes().toString().padStart(2, '0');
    return hours+":"+minutes;
  }

  getRepeatingString(alarm: Alarm): string {
    let repeatString: string = "";
    if (alarm.regular) {
      repeatString += "jeden "
    }

    if (alarm.monday && alarm.tuesday && alarm.wednesday && alarm.thursday && alarm.friday) {
      if (alarm.saturday && alarm.sunday) {
        repeatString += "Tag"
      } else if (!alarm.saturday && !alarm.sunday) {
        repeatString += "Wochentag"
      }
    } else {
      if (alarm.monday) {
      repeatString += "Montag, ";
      }
      if (alarm.tuesday) {
        repeatString += "Dienstag, ";
      }
      if (alarm.wednesday) {
        repeatString += "Mittwoch, ";
      }
      if (alarm.thursday) {
        repeatString += "Donnerstag, ";
      }
      if (alarm.friday) {
        repeatString += "Freitag, ";
      }
      if (alarm.saturday) {
        repeatString += "Samstag, ";
      }
      if (alarm.sunday) {
        repeatString += "Sonntag, ";
      }
    }
    return this.rtrim(repeatString, ", ");
  }

  rtrim(input: string, characters: string): string {
    let start = 0;
    let end = input.length - 1;
    while (characters.indexOf(input[end]) >= 0) {
      end -= 1;
    }
    return input.substr(0, end + 1);
  }
}